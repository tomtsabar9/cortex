import socket
from datetime import datetime
import time
import threading
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
        user_msg_data = self.conn.receive()
    
        user = UserMsg()
        user.ParseFromString(user_msg_data)
        print (user)
        snapshot_msg_data = self.conn.receive()
        snapshot = SnapshotMsg.ParseFromString(snapshot_msg_data)

        self.conn.close()



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

