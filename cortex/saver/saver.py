from .. import MsgQueue
import sqlalchemy as db
from sqlalchemy.sql import text
from sqlalchemy.sql import select

from pathlib import Path
import json 

from .. import get_table
from .. import random_string



def saver_factory():
    """
    Packs all type savers in single dictionary
    TODO - change to more beutifull way
    """
    savers = dict()

  
    def callback(ch, method, properties, body):

        suffix, data = body.decode("utf-8").split(":", 1)
               

        if suffix == 'user':
            if (user_saver(data, savers["db"])):
                ch.basic_ack(delivery_tag = method.delivery_tag)
        elif suffix == 'snapshot':
            if (snapshot_saver(data, savers["db"])):
                ch.basic_ack(delivery_tag = method.delivery_tag)
        else:
            path = Path(suffix)

            time = path.name
            parser = path.parent.name
            user_id = path.parent.parent.name

            print (parser)
            if (raw_data_saver(parser, user_id, time, data, savers["queue"], savers["db"])):
                ch.basic_ack(delivery_tag = method.delivery_tag)


    def snapshot_saver(snap_json, cortex_db):

        snapshot_user = json.loads(snap_json)

        connection = cortex_db.connect()
        metadata = db.MetaData()

        snapshots_table = get_table(metadata, 'snapshots')
        metadata.create_all(cortex_db)

        s = select([snapshots_table]).where(snapshots_table.c.Id == int(snapshot_user['user_id'])).where(snapshots_table.c.Date == int(snapshot_user['snapshot_date']))
        result = connection.execute(s).fetchone()
  
        if result is None:
            insert = db.insert(snapshots_table).values(Uid=random_string(), Id=int(snapshot_user['user_id']), Date=int(snapshot_user['snapshot_date']), Results=snapshot_user['results'])
            ResultProxy = connection.execute(insert)
        return True
       
    def user_saver(user_json, cortex_db):

        user = json.loads(user_json)

        connection = cortex_db.connect()
        metadata = db.MetaData()

        users_table = get_table(metadata, 'users')
        metadata.create_all(cortex_db)

        s = select([users_table]).where(users_table.c.Id == int(user['user_id']))
        result = connection.execute(s).fetchone()
  
        if result is None:
            insert = db.insert(users_table).values(Id=int(user['user_id']), Name=user['username'], Birth=int(user['birthday']), Gender=user['gender']) 
            ResultProxy = connection.execute(insert)
        return True

    def raw_data_saver(parser, user_id, time, data, msgQueue, cortex_db):

        msgQueue.add_queue('raw_data')

        connection = cortex_db.connect()
        metadata = db.MetaData()

        emp = get_table(metadata, parser)

        metadata.create_all(cortex_db)

        query = db.insert(emp).values(Id=int(user_id), Date=(time), Data=data) 
        ResultProxy = connection.execute(query)
        return True

    savers['callback'] = callback
    return savers
