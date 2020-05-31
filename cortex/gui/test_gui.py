from .. import get_table
import tempfile

from .gui import create_gui
from . import DummyRequests

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.sql import select

import json
import pytest

SQLLITE = 'sqlite:///'
TMP_DB_FILE = 'tmp.db'
DB_PATH = 'db_path'

@pytest.fixture
def client(tmp_path):
    

    responses = dict()
    responses['users'] = {"42": "Dan Gittik", "6262": "Tom Tsabar", "1234": "Tom hh"}
    responses['42'] = {"user_id": 42, "username": "Dan Gittik", "birthday": 699746400, "gender": 0}
    responses['snapshots'] = {"srqoninifyvaxckw": 1575446887339}
    responses['srqoninifyvaxckw'] = {"id": "srqoninifyvaxckw", "time": 1575446887339, "options": ["pose", "color_image", "depth_image"]}
    responses['pose'] = {"px": 0.4873843491077423, "py": 0.007090016733855009, "pz": -1.1306129693984985, "rx": -0.10888676356214629, "ry": -0.26755994585035286, "rz": -0.021271118915446748, "rw": 0.9571326384559261}
    responses['color_image'] = '/home/user/Desktop/cortex/data/cortex data/42/color_image/1575446887339.png'


    requests = DummyRequests(responses)
    tmp_file = str (tmp_path / TMP_DB_FILE)
    db_path = f'{SQLLITE}{tmp_file}'
    app = create_gui('127.0.0.1', 1337, requests)
    
    app.config['TESTING'] = True

    with app.test_client() as client:
        client.__dict__[DB_PATH] = db_path
        yield client


def test_index(client):
    """Start with a blank database."""

    response = client.get('/')

    assert '200 OK' == response._status
    assert b'Dan Gittik' in response.data


def test_show(client):
    """Start with a blank database."""

    response = client.get('/show/42?user_name=Yoko%20Ono')

    assert '200 OK' == response._status
    assert b'Yoko Ono' in response.data
    assert b'srqoninifyvaxckw/pose' in response.data
    assert b'srqoninifyvaxckw/color_image' in response.data