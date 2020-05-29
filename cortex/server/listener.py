from .. import Connection
import socket

class Listener:
    """
    Wraps server basic behavior
    """
    def __init__(self, host = "0.0.0.0", port=8000, backlog = 1000, reuseaddr = True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()
    def __repr__(self):
        return f"Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})"

    def start(self):
        self.server = socket.socket()

        if (self.reuseaddr):
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server.bind((self.host, self.port))

        self.server.listen(self.backlog)

    def accept(self):
        client, far_addr = self.server.accept()
        return Connection(client)
    def stop(self):
        self.server.close()
