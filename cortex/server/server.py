import socket
from datetime import datetime
import time
import threading
import pika

from pathlib import Path

from .. import UserMsg
from .. import SnapshotMsg
from .. import MsgQueue
from .. import parsers

class Handler(threading.Thread):
    """
    Handles client request
    """

    def __init__(self, conn, queue_url):
        super().__init__()
        self.conn = conn
        self.msgQueue = MsgQueue(queue_url)

        self.msgQueue.add_exchange('parsers', 'fanout')
        for key in parsers.keys():
            self.msgQueue.bind_exchange('parsers', key)
  
        
    def run(self):
        

        with self.conn as connection:
            user_msg_data = connection.receive()

            user = UserMsg()
            user.ParseFromString(user_msg_data)
            print (user)

            
            while 1:
                try:

                    snapshot = SnapshotMsg()
                    snapshot_msg_data = connection.receive()

                    snapshot.ParseFromString(snapshot_msg_data)


                    self.msgQueue.publish(ex_name='parsers',q_name='', msg=str(snapshot.datetime))

                    print ("got snap")
                except Exception as e:
                    print (e)
                    break

