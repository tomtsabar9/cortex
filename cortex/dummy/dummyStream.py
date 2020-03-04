class DummyStream:

    def __init__(self, rdata = ''):
        self.rdata = rdata
    def write(self, data):
        self.wrote = data
    def read(self, size):
        ret = self.rdata[:size]
        self.rdata = self.rdata[size:]
        return ret