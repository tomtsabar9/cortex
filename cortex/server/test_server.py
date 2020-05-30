from .server import Handler
from . import DummyStream
from . import DummyConn
from . import DummyQueue
from .. import UserMsg
from .. import SnapshotMsg
from .. import ColorImageMsg
from .. import FeelingsMsg

import pytest


@pytest.fixture
def basic_handler(tmp_path):
    conn = DummyConn('')
    return Handler(conn, tmp_path, "dummy://", None)



def test_save_user_data(basic_handler):
    
    basic_handler.msgQueue = DummyQueue()
    user = UserMsg()
    user.ParseFromString(b'\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02')

    basic_handler.save_user_data(user)

    json_msg = 'user:{"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0}'
    assert basic_handler.msgQueue.ex_name == ''
    assert basic_handler.msgQueue.queues['raw_data'] == json_msg


def test_save_snapshot_meta(basic_handler):
    
    basic_handler.msgQueue = DummyQueue()
    user_id = 1337
    snapshot_date = 254724572457
    results = ['yo', 'mo', 'ho']
    basic_handler.save_snapshot_meta(user_id, snapshot_date, results)

    json_msg = 'snapshot:{"user_id": 1337, "snapshot_date": 254724572457, "results": "[\\"yo\\", \\"mo\\", \\"ho\\"]"}'
    assert basic_handler.msgQueue.ex_name == ''
    assert basic_handler.msgQueue.queues['raw_data'] == json_msg
    

def test_save_data_for_parsers(basic_handler):
    
    snapshot = SnapshotMsg()

    snapshot.feelings.hunger = 0.1
    snapshot.feelings.thirst = 0.2
    snapshot.feelings.exhaustion = 0.3
    snapshot.feelings.happiness = 0.4

    snapshot.color_image.width = 1
    snapshot.color_image.height = 1
    snapshot.color_image.data = b'5'
    
    parsers = basic_handler.save_data_for_parsers(snapshot)

    assert 'pose' not in parsers
    assert 'color_image' in parsers
    assert 'depth_image' not in parsers
    assert 'feelings' in parsers

def test_save_snapshot_submsg(basic_handler):
    
    snapshot = SnapshotMsg()

    snapshot.datetime = 1234

    snapshot.feelings.hunger = 0.1
    snapshot.feelings.thirst = 0.2
    snapshot.feelings.exhaustion = 0.3
    snapshot.feelings.happiness = 0.4

    snapshot.color_image.width = 1
    snapshot.color_image.height = 1
    snapshot.color_image.data = b'5'

    result_f = basic_handler.save_snapshot_submsg(snapshot, 'feelings')
    result_c = basic_handler.save_snapshot_submsg(snapshot, 'color_image')
    result_d = basic_handler.save_snapshot_submsg(snapshot, 'depth_image')
    result_p = basic_handler.save_snapshot_submsg(snapshot, 'pose')

    assert result_f == True
    assert result_c == True
    assert result_d == False
    assert result_p == False

    path = basic_handler.root / 'feelings' / '1234'

    data = path.read_bytes()

    assert data == snapshot.feelings.SerializeToString()

