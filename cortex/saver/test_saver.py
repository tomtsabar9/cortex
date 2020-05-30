from .saver import save
from .. import get_table

from . import DummyQueue

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.sql import select

import pytest

def test_save_user(tmp_path):
    
    data = '{"user_id": 6262, "username": "Tom hh", "birthday": 6997346400, "gender": 1}'
   
    tmp_file = tmp_path / 'tmp.db'
    db_url = 'sqlite:///'+str(tmp_file)
    save(db_url, 'user', data)

    cortex_db = db.create_engine(db_url)
    connection = cortex_db.connect()
    metadata = db.MetaData()

    users_table = get_table(metadata, 'users')

    s = select([users_table])
    user = connection.execute(s).fetchone()
        

    assert user[0]==6262
    assert user[1]=="Tom hh"
    assert user[2]==6997346400
    assert user[3]=='1'

def test_save_snapshot(tmp_path):
    
    data = '{"user_id": 42, "snapshot_date": 1575446887339, "results": "[\\"pose\\", \\"color_image\\", \\"depth_image\\"]"}'
   
    tmp_file = tmp_path / 'tmp.db'
    db_url = 'sqlite:///'+str(tmp_file)
    save(db_url, 'snapshot', data)

    cortex_db = db.create_engine(db_url)
    connection = cortex_db.connect()
    metadata = db.MetaData()

    snaps_table = get_table(metadata, 'snapshots')

    s = select([snaps_table])
    user = connection.execute(s).fetchone()
        
    assert user[1]==42
    assert user[2]==1575446887339
    assert user[3]=="[\"pose\", \"color_image\", \"depth_image\"]"


def test_save_pose(tmp_path):
    
    data = '{"px": 0.4873843491077423, "py": 0.007090016733855009, "pz": -1.1306129693984985, "rx": -0.10888676356214629, "ry": -0.26755994585035286, "rz": -0.021271118915446748, "rw": 0.9571326384559261}'
   
    tmp_file = tmp_path / 'tmp.db'
    db_url = 'sqlite:///'+str(tmp_file)
    save(db_url, '/home/user/Desktop/cortex/data/cortex data/42/pose/1575446887339', data)

    cortex_db = db.create_engine(db_url)
    connection = cortex_db.connect()
    metadata = db.MetaData()

    pose_table = get_table(metadata, 'pose')

    s = select([pose_table])
    user = connection.execute(s).fetchone()
 
    assert user[0]==42
    assert user[1]==1575446887339
    assert user[2]==data

