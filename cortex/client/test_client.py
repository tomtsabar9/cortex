from .client import send_serialized_data
from .client import proto_formater
from .client import get_reader
from .client import send_user_data
from .client import send_snapshot
from . import DummyStream
from . import DummyConn

import gzip

def test_send_serial():
    raw_data = b'\x14\x00\x00\x00\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02'
    stream = DummyStream(raw_data)
    conn = DummyConn()
    send_serialized_data(conn, stream, proto_formater)

    assert conn.sent == raw_data[4:]

def test_user_data():
    raw_data = b'\x14\x00\x00\x00\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02'
    stream = DummyStream(raw_data)
    conn = DummyConn()
    send_user_data(conn, stream, 'proto')

    assert conn.sent == raw_data[4:]

def test_snapshot():
    raw_data = b'JustRandomData'
    stream = DummyStream(raw_data)
    conn = DummyConn()
    send_snapshot(conn, stream, 'proto')

    assert conn.sent == raw_data[4:]

def test_get_reader(tmp_path):
    file_path = tmp_path / 'tmp'
    file_path.write_bytes(b'1234')

    gz_type = type(gzip.open(file_path,'rb'))
    text_type = type(open(file_path, 'rb'))
    assert text_type == type(get_reader(file_path, 'text'))
    assert gz_type == type(get_reader(file_path, 'gz'))

    assert text_type != type(get_reader(file_path, 'gz'))
    assert gz_type != type(get_reader(file_path, 'text'))
