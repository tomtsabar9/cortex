import socket
from datetime import datetime
import time
import threading
import pika

from pathlib import Path

from .. import UserMsg
from .. import SnapshotMsg
from .. import PoseMsg
from .. import ColorImageMsg
from .. import DepthImageMsg
from .. import FeelingsMsg


from .. import MsgQueue
from .. import parsers

class Handler(threading.Thread):
    """
    Handles client request
    """

    def __init__(self, conn, root, queue_url):
        super().__init__()
        self.conn = conn
        self.root = Path(root)
        self.msgQueue = MsgQueue(queue_url)

        self.root = self.root / 'cortex data'
        self.root.mkdir(parents=True, exist_ok=True)

        self.msgQueue.add_exchange('parsers', 'fanout')
        for key in parsers.keys():
            self.msgQueue.bind_exchange('parsers', key)
  
        
    def save_user_data(self, user):
        self.root = self.root / str(user.user_id)
        self.root.mkdir(parents=True, exist_ok=True)

        self.user_details = self.root / "details.txt"
        self.user_details.write_bytes(user.SerializeToString())

    def save_snapshot_submsg(self, snapshot, submsg_type):
        self.submsg_dir = self.root / submsg_type
        self.submsg_dir.mkdir(parents=True, exist_ok=True)
      
        submsg = getattr(snapshot, submsg_type)
        self.submsg_file = self.submsg_dir / str(snapshot.datetime)
        self.submsg_file.write_bytes(submsg.SerializeToString())

    def run(self):
        with self.conn as connection:
            user_msg_data = connection.receive()

            user = UserMsg()
            user.ParseFromString(user_msg_data)
            
            self.save_user_data(user)

            
            while 1:
                try:

                    snapshot = SnapshotMsg()
                    snapshot_msg_data = connection.receive()

                    snapshot.ParseFromString(snapshot_msg_data)

                    self.save_snapshot_submsg(snapshot, "pose")
                    self.msgQueue.publish(ex_name='parsers',q_name='', msg=str(snapshot.datetime))

                    print ("got snap")
                except Exception as e:
                    print (e)
                    break

