from urllib.parse import urlparse
from pathlib import Path

class MyJsonWrapper:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


class DummyRequests:
    def __init__(self, responses):
        self.responses = responses

    def get(self, url):
        purl = urlparse(url)
        
        req = Path(purl.path)

        response = self.responses[req.name]
        if type(response) == type(dict()):
            return MyJsonWrapper(self.responses[req.name])
        else:
            self.responses[req.name]
        

