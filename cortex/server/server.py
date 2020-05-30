import socket
from datetime import datetime
import time
import threading
import pika
import json

from pathlib import Path

from .. import UserMsg
from .. import SnapshotMsg
from .. import PoseMsg
from .. import ColorImageMsg
from .. import DepthImageMsg
from .. import FeelingsMsg


from .. import MsgQueue


class Handler(threading.Thread):
    """
    Handles client requests, parsing each request and passing information to the right queues.
    """

    def __init__(self, conn, root, queue_url):
        super().__init__()
        self.stop_event = threading.Event()
        self.conn = conn
        self.root = Path(root)
        self.msgQueue = MsgQueue(queue_url)

        self.root = self.root / 'cortex data'
        self.root.mkdir(parents=True, exist_ok=True)

        self.msgQueue.add_exchange('parsers', 'fanout')
        self.parsers = self.get_parsers()

        for key in self.parsers:
            self.msgQueue.bind_exchange('parsers', key)
  
    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def get_parsers(self):
        parsers = []
        for item in SnapshotMsg.__dict__.items():
            if not 'FieldProperty' in str(type(item[1])):
                continue
            if 'datetime' in item[0]:
                continue

            parsers.append (item[0])
        return parsers

    def save_user_data(self, user):
        self.root = self.root / str(user.user_id)
        self.root.mkdir(parents=True, exist_ok=True)

        user_json = json.dumps(dict(
                user_id = user.user_id,
                username = user.username,
                birthday = user.birthday,
                gender = user.gender
                ))

        self.msgQueue.publish(ex_name='',q_name='raw_data', msg='user:'+user_json)

    def save_snapshot_meta(self, user_id, snapshot_date, results):
        snap_json = json.dumps(dict(
                user_id = user_id,
                snapshot_date = snapshot_date,
                results = json.dumps(results)
                ))


        self.msgQueue.publish(ex_name='',q_name='raw_data', msg='snapshot:'+snap_json)

    def save_data_for_parsers(self, snapshot):
        succesful_parsers = []
        for key in self.parsers:
            if self.save_snapshot_submsg(snapshot, key):
                succesful_parsers.append(key)

        return succesful_parsers

    def save_snapshot_submsg(self, snapshot, submsg_type):
        try:
            self.submsg_dir = self.root / submsg_type
            self.submsg_dir.mkdir(parents=True, exist_ok=True)
          
            submsg = getattr(snapshot, submsg_type)
            if repr(submsg) == "":
                return False

            self.submsg_file = self.submsg_dir / str(snapshot.datetime)
            self.submsg_file.write_bytes(submsg.SerializeToString())

            return True
        except:
            return False

    def run(self):

        with self.conn as connection:
            user_msg_data = connection.receive()

            user = UserMsg()
            user.ParseFromString(user_msg_data)

            if self.stopped():
                return
            self.save_user_data(user)

                
            while 1:

                try:
                    snapshot = SnapshotMsg()
                    
                    if self.stopped():
                        return

                    print ("1")
                    snapshot_msg_data = connection.receive()
                    print ("2")
                    snapshot.ParseFromString(snapshot_msg_data)
                    print ("3")
                    results = self.save_data_for_parsers(snapshot)
                    print ("4")
                    self.msgQueue.publish(ex_name='parsers',q_name='', msg=str(self.root.absolute())+":"+str(snapshot.datetime))
                    print ("5")
                    self.save_snapshot_meta(user.user_id, snapshot.datetime, results)
                    print ("6")
                    print ("got a snapshot")
                except :
                    print ("client disconnected")
                    return

                    



