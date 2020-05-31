from .. import MsgQueue
import sqlalchemy as db
from sqlalchemy.sql import text
from sqlalchemy.sql import select

from pathlib import Path
import json 
import os

from .. import get_table
from .. import random_string

all_savers = dict()

def saver(name):
    def decorator(save_function):
        all_savers[name] = save_function
        return save_function
    return decorator

def run_saver(db_url, queue_url):
     
    print ('Saver starting...')
    msgQueue = MsgQueue(queue_url)
    msgQueue.add_queue('raw_data')

    callback = saver_queue_factory(msgQueue, db_url)

    msgQueue.add_consumer('raw_data', callback)
    msgQueue.consume()
    
def save(database, data_type, data):

    username = os.environ.get('_USERNAME')
    password = os.environ.get('_PASSWORD')

    if 'postgresql' in database:
        database = database.replace('://', '://'+username+':'+password+'@')
        cortex_db = db.create_engine(database, pool_size=50, max_overflow=0)
    else:
        cortex_db = db.create_engine(database)
    

    if data_type in all_savers.keys():
        all_savers[data_type](data, cortex_db)
    else:
        #The path defualt "data_type" holds its dynamic type as the path of its parser data
        path = Path(data_type)

        time = path.name
        parser = path.parent.name
        user_id = path.parent.parent.name

        raw_saver(parser, user_id, time, data, cortex_db)

    return True

@saver('user')
def user_saver(user_json, cortex_db):

    connection = cortex_db.connect()
    metadata = db.MetaData()

    user = json.loads(user_json)

    users_table = get_table(metadata, 'users')
    metadata.create_all(cortex_db)

    s = select([users_table]).where(users_table.c.Id == int(user['user_id']))
    result = connection.execute(s).fetchone()
  
    if result is None:
        insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
        connection.execute(insert)

    return True

@saver('snapshot')
def snapshot_saver(snap_json, cortex_db):

    connection = cortex_db.connect()
    metadata = db.MetaData()

    snapshot_user = json.loads(snap_json)

    snapshots_table = get_table(metadata, 'snapshots')
    metadata.create_all(cortex_db)

    s = select([snapshots_table]).where(snapshots_table.c.Id == int(snapshot_user['user_id'])).where(snapshots_table.c.Date == int(snapshot_user['snapshot_date']))
    result = connection.execute(s).fetchone()
  
    if result is None:
        insert = db.insert(snapshots_table).values(Uid=random_string(), Id=int(snapshot_user['user_id']), Date=int(snapshot_user['snapshot_date']), Results=snapshot_user['results'])
        connection.execute(insert)

    return True

@saver('raw_saver')
def raw_saver(parser, user_id, time, data, cortex_db):
    """
    Dynamic saver for all parsers
    """
    connection = cortex_db.connect()
    metadata = db.MetaData()

    parser_table = get_table(metadata, parser)
    metadata.create_all(cortex_db)

    s = select([parser_table]).where(parser_table.c.Id == int(user_id)).where(parser_table.c.Date == time)
    result = connection.execute(s).fetchone()
  
    if result is None:
        insert = db.insert(parser_table).values(Id=int(user_id), Date=(time), Data=data) 
        connection.execute(insert)

    return True



def saver_queue_factory(msgQueue, db_url):
    """
    Wraps the savers and reacts with msg queue
    """
  
    def callback(ch, method, properties, body):

        suffix, data = body.decode("utf-8").split(":", 1)
               
        if (save(db_url, suffix, data)):
            ch.basic_ack(delivery_tag = method.delivery_tag)
                

    return callback
