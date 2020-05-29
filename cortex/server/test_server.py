from .server import Handler
from . import DummyStream
from . import DummyConn
from . import DummyQueue
from .. import UserMsg

import pytest


@pytest.fixture
def basic_handler(tmp_path):
    conn = DummyConn('')
    return Handler(conn, tmp_path, "dummy://")



def test_save_user_data(basic_handler):
    
    basic_handler.msgQueue = DummyQueue()
    user = UserMsg()
    user.ParseFromString(b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02')

    basic_handler.save_user_data(user)

    assert basic_handler.msgQueue.ex_name == ""
    assert basic_handler.msgQueue.q_name == "raw_data"
    assert basic_handler.msgQueue.msg == 'user:{"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0}'
