import socket
from datetime import datetime
import time
import threading
import pika

from pathlib import Path
from .listener import Listener

from .. import UserMsg
from .. import SnapshotMsg

class Handler(threading.Thread):
    """
    Handles client request
    """

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
  
        
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

                    credentials = pika.PlainCredentials('guest', 'guest')
                    pconnection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
                    msgChannel = pconnection.channel()
                    msgChannel.queue_declare(queue='users')
                    msgChannel.basic_publish(exchange='',
                        routing_key='users',
                        body='Hello World!')

                    pconnection.close()
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

