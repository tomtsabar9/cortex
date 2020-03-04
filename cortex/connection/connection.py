import socket
import struct

class Connection:
    """
    TODO doc
    """
    def __init__(self, socket):
        self.socket = socket
    def __enter__(self):
        return self
    def __exit__(self, exception, error, traceback):
        self.socket.close()

    def send(self, data):
        return self.socket.send(struct.pack('<I', len(data)) + data)

    def receive(self):
        data = b''
        size = struct.unpack('<I', self.socket.recv(4))[0]   
       
        while (size > 0):
            recv = self.socket.recv(size)
            size -= len(recv)
            data += recv

        return data

    @classmethod
    def connect(cls, ip, port):
        conn = socket.socket()
        conn.connect((ip, port))

        return Connection(conn)