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

from .listener import Listener

def run_server(host, port, queue_url='rabbitmq://127.0.0.1:5672/', root='data',handlers = None, publish = None):
    """
    Listen to incoming client connections, parse them and prints the msg
    """

    print ("Server starting...")

    server = Listener(host, port)
    
    server.start()

    while 1:  

        try:
            client = server.accept()

            handler = Handler(client, root, queue_url, publish)
            print ("client connected")
            handler.start()
            handlers.append(handler)

        except Exception as e:
            print (e)
            break

class OuterQueue:
    def __init__(self, publish_func):
        self.publish_func = publish_func

    def publish(self, *args, **kwargs):
        self.publish_func((args,kwargs))


class Handler(threading.Thread):
    """
    Handles client requests, parsing each request and passing information to the right queues.
    """

    def __init__(self, conn, root, queue_url, publish):
        super().__init__()
        self.stop_event = threading.Event()

        self.conn = conn
        self.root = Path(root)
    
        self.root = self.root / 'cortex data'
        self.root.mkdir(parents=True, exist_ok=True)

        self.parsers = self.get_parsers()

        if publish != None:
            self.msgQueue = OuterQueue(publish)
        else:
            self.msgQueue = MsgQueue(queue_url)
            self.msgQueue.add_exchange('parsers', 'fanout')
            for key in self.parsers:
                self.msgQueue.bind_exchange('parsers', key)

            self.msgQueue.add_queue('raw_data')

        
  
    def stop(self):
        """

        """
        self.stop_event.set()

    def stopped(self):
        """
         
        """
        return self.stop_event.is_set()

    def get_parsers(self):
        """
        Get parsers from protobuf object.
        If future sub-snapshot will be added they will be automaticly parsed and published.
        """
        parsers = []
        for item in SnapshotMsg.__dict__.items():
            if not 'FieldProperty' in str(type(item[1])):
                continue
            if 'datetime' in item[0]:
                continue

            parsers.append (item[0])
        return parsers

    def save_user_data(self, user):
        """
        Publish user details
        """
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
        """
        Publish snapshot metadata
        """
        snap_json = json.dumps(dict(
                user_id = user_id,
                snapshot_date = snapshot_date,
                results = json.dumps(results)
                ))


        self.msgQueue.publish(ex_name='',q_name='raw_data', msg='snapshot:'+snap_json)

    def save_data_for_parsers(self, snapshot):
        """
        Check and write data for available parses
        """
        succesful_parsers = []
        for key in self.parsers:
            if self.save_snapshot_submsg(snapshot, key):
                succesful_parsers.append(key)

        return succesful_parsers

    def save_snapshot_submsg(self, snapshot, submsg_type):
        """
        Save sub messesge of snapshot in file, before passed to parser
        """
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

                    snapshot_msg_data = connection.receive()
                    snapshot.ParseFromString(snapshot_msg_data)

                    results = self.save_data_for_parsers(snapshot)
                    
                    self.msgQueue.publish(ex_name='parsers',q_name='', msg=str(self.root.absolute())+":"+str(snapshot.datetime))

                    self.save_snapshot_meta(user.user_id, snapshot.datetime, results)

                    print ("got a snapshot")
                except :
                    print ("client disconnected")
                    return

                    



