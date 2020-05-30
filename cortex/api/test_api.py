from .. import get_table
import tempfile

from .api import create_api

import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.sql import select

import json
import pytest

@pytest.fixture
def client(tmp_path):
    
    tmp_file = tmp_path / 'tmp.db'
    db_path = 'sqlite:///'+str(tmp_file)
    app = create_api(db_path)
    
    app.config['TESTING'] = True

    with app.test_client() as client:
        client.__dict__['db_path'] = db_path
        yield client


def test_empty_db(client):
    """Start with a blank database."""

    response = client.get('/users')

    assert '200 OK' == response._status
    assert b'{}' == response.data

def test_2_users(client):
    """Add 2 users to db."""

    tmp_db = db.create_engine(client.__dict__['db_path'])
    connection = tmp_db.connect()
    metadata = db.MetaData()

    users_table = get_table(metadata, 'users')
    metadata.create_all(tmp_db)

    user = json.loads('{"user_id": 1234, "username": "Israel Eliras", "birthday": 6997346400, "gender": 1}')
    insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
    connection.execute(insert)

    user = json.loads('{"user_id": 4321, "username": "Eliras Israel", "birthday": 6997346401, "gender": 0}')
    insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
    connection.execute(insert)

    response = client.get('/users')

    assert '200 OK' == response._status
    assert b'{"1234": "Israel Eliras", "4321": "Eliras Israel"}' == response.data

def test_user(client):
    """Test view full details of singel user."""

    tmp_db = db.create_engine(client.__dict__['db_path'])
    connection = tmp_db.connect()
    metadata = db.MetaData()

    users_table = get_table(metadata, 'users')
    metadata.create_all(tmp_db)

    user = json.loads('{"user_id": 1234, "username": "Israel Eliras", "birthday": 6997346400, "gender": 1}')
    insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
    connection.execute(insert)

    response = client.get('/users/1234')

    assert '200 OK' == response._status
    assert b'{"user_id": 1234, "username": "Israel Eliras", "birthday": 6997346400, "gender": 1}' == response.data


def test_snapshots_single(client):
    """Test listing off all snapshots of single user"""

    tmp_db = db.create_engine(client.__dict__['db_path'])
    connection = tmp_db.connect()
    metadata = db.MetaData()

    users_table = get_table(metadata, 'users')
    snapshots_table = get_table(metadata, 'snapshots')

    metadata.create_all(tmp_db)

    user = json.loads('{"user_id": 1234, "username": "Israel Eliras", "birthday": 6997346400, "gender": 1}')
    insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
    connection.execute(insert)

    snapshot_user = json.loads('{"user_id": 1234, "snapshot_date": 1575446887339, "results": "[\\"pose\\", \\"color_image\\", \\"depth_image\\"]"}')
    insert = db.insert(snapshots_table).values(Uid="123456789ABCDEF", Id=int(snapshot_user['user_id']), Date=int(snapshot_user['snapshot_date']), Results=snapshot_user['results'])
    connection.execute(insert)

    response = client.get('/users/1234/snapshots')

    assert '200 OK' == response._status
    assert b'{"123456789ABCDEF": 1575446887339}' == response.data

def test_snapshot(client):
    """Test view of details of specific snapshot"""

    tmp_db = db.create_engine(client.__dict__['db_path'])
    connection = tmp_db.connect()
    metadata = db.MetaData()

    users_table = get_table(metadata, 'users')
    snapshots_table = get_table(metadata, 'snapshots')

    metadata.create_all(tmp_db)

    user = json.loads('{"user_id": 1234, "username": "Israel Eliras", "birthday": 6997346400, "gender": 1}')
    insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
    connection.execute(insert)

    snapshot_user = json.loads('{"user_id": 1234, "snapshot_date": 1575446887339, "results": "[\\"pose\\", \\"depth_image\\"]"}')
    insert = db.insert(snapshots_table).values(Uid="123456789ABCDEF", Id=int(snapshot_user['user_id']), Date=int(snapshot_user['snapshot_date']), Results=snapshot_user['results'])
    connection.execute(insert)

    response = client.get('/users/1234/snapshots/123456789ABCDEF')

    assert '200 OK' == response._status
    assert b'{"id": "123456789ABCDEF", "time": 1575446887339, "options": ["pose", "depth_image"]}' == response.data


def test_result(client):
    """Test view of details of specific snapshot"""

    tmp_db = db.create_engine(client.__dict__['db_path'])
    connection = tmp_db.connect()
    metadata = db.MetaData()

    users_table = get_table(metadata, 'users')
    snapshots_table = get_table(metadata, 'snapshots')
    parser_table = get_table(metadata, 'pose')
    metadata.create_all(tmp_db)

    user = json.loads('{"user_id": 1234, "username": "Israel Eliras", "birthday": 6997346400, "gender": 1}')
    insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
    connection.execute(insert)

    snapshot_user = json.loads('{"user_id": 1234, "snapshot_date": 1575446887339, "results": "[\\"pose\\", \\"depth_image\\"]"}')
    insert = db.insert(snapshots_table).values(Uid="123456789ABCDEF", Id=int(snapshot_user['user_id']), Date=int(snapshot_user['snapshot_date']), Results=snapshot_user['results'])
    connection.execute(insert)

    insert = db.insert(parser_table).values(Id=1234, Date=1575446887339, Data='Test Test Test') 
    connection.execute(insert)

    response = client.get('/users/1234/snapshots/123456789ABCDEF/pose')

    assert '200 OK' == response._status
    assert b'Test Test Test' == response.data


    
    