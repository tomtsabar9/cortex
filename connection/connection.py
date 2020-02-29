import socket
import struct

class Connection:

    def __init__(self, socket):
        self.socket = socket
    def __enter__(self):
        return self
    def __exit__(self, exception, error, traceback):
        self.socket.close()

    def send(self, data):
        return self.socket.send(struct.pack('<I', len(data)) + data)

    def receive(self):
        size = struct.unpack('<I', self.socket.recv(4))[0]   
        return self.socket.recv(size)

    @classmethod
    def connect(cls, ip, port):
        conn = socket.socket()
        conn.connect((ip, port))

        return Connection(conn)
