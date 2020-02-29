class DummyConn:

    def __init__(self, rdata = ''):
        self.rdata = rdata
    def send(self, data):
        self.sent = data
    def recieve(self):
        return self.rdata