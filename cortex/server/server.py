import socket
from datetime import datetime
import time
import threading
import pika

from pathlib import Path
from .listener import Listener

from .. import UserMsg
from .. import SnapshotMsg
from .. import MsgQueue
from .. import parsers

class Handler(threading.Thread):
    """
    Handles client request
    """

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
  
        
    def run(self):
        queue_url = 'rabbitmq://127.0.0.1:5672/'
        msgQueue = MsgQueue(queue_url)
        msgQueue.add_exchange('parsers', 'fanout')
        print (repr(parsers))
        for key in parsers.keys():
            msgQueue.bind_exchange('parsers', key)
            print ("key: ", key)

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


                    msgQueue.publish(ex_name='parsers',q_name='', msg='Hello World!')

                    print ("got snap")
                except Exception as e:
                    print (e)
                    break

def run(host, port):
    """
    Listen to incoming client connections, parse them and prints the msg
    """
    server = Listener(host, int(port))
    
    server.start()

    

    while (1):  
        client = server.accept()
        handler = Handler(client)
        handler.start()
          
    server.stop()

