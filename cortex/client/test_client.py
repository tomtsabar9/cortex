from .__main__ import send_serialized_data
from .__main__ import proto_formater
from . import DummyStream
from . import DummyConn

def test_send_serial():
	raw_data = b'\x14\x00\x00\x00\x08*\x12\nDan Gittik\x18\xe0\x90\xd5\xcd\x02'
	stream = DummyStream(raw_data)
	conn = DummyConn()
	send_serialized_data(conn, stream, proto_formater)

	assert conn.sent == raw_data[4:]
