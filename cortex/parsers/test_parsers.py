from .parsers import parser_factory
from . import DummyQueue

import pytest



def test_pose_parser(tmp_path):
    
    parsers = parser_factory()
    pose_parser = parsers['pose_orig']

    pose_path = tmp_path / "pose"
    pose_path.mkdir()
    pose_file = pose_path / "tmp"
    pose_file.write_bytes(b'\n\x1b\t\x00\x00\x00\xc0\xf1h\xb5\xbf\x11\x00\x00\x00@\xa4\xc3\xa0?\x19\x00\x00\x00`+r\xdc?\x12$\t\xee\x90S(\xbe\xb5\xc7\xbf\x11,\x1f\x8d\xa8\xa2Y\x88\xbf\x19\xb8\\Vh\xb4\xbd\x87?!G\xab\nk\x15q\xef?')

    msgQueue = DummyQueue()
    pose_parser(pose_file, msgQueue)

    json_msg = str(pose_file)+':{"px": -0.08363257348537445, "py": 0.03274262696504593, "pz": 0.44446834921836853, "rx": -0.18523385018409705, "ry": -0.011889715927864218, "rz": 0.01159230178272562, "rw": 0.9825541582734808}'
    assert msgQueue.ex_name == ""
    assert msgQueue.queues["raw_data"] == json_msg


def test_feelings_parser(tmp_path):
    
    parsers = parser_factory()
    pose_parser = parsers['feelings_orig']

    pose_path = tmp_path / "feelings"
    pose_path.mkdir()
    pose_file = pose_path / "tmp"
    pose_file.write_bytes(b'\ro\x12\x83:\x15\xa6\x9bD;\x1do\x12\x03;')

    msgQueue = DummyQueue()
    pose_parser(pose_file, msgQueue)

    json_msg = str(pose_file)+':{"hunger": 0.0010000000474974513, "thirst": 0.003000000026077032, "exhaustion": 0.0020000000949949026, "happiness": 0.0}'

    assert msgQueue.ex_name == ""
    assert msgQueue.queues["raw_data"] == json_msg