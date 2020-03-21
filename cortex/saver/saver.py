from .. import MsgQueue
import sqlalchemy as db
from pathlib import Path

def saver_factory():

    savers = dict()

    def saver(name):
        def decorator(save_function):
            def callback(ch, method, properties, body):

                path, data = body.decode("utf-8").split(":", 1)
               
                path = Path(path)

                time = path.name
                parser = path.parent.name
                user_id = path.parent.parent.name

                if (save_function(parser, user_id, time, data, savers["queue"], savers["db"])):
                    ch.basic_ack(delivery_tag = method.delivery_tag)

            savers[name] = callback
        return decorator

    @saver('raw_data')
    def raw_data_saver(parser, user_id, time, data, msgQueue, cortex_db):

        msgQueue.add_queue('raw_data')

        connection = cortex_db.connect()
        metadata = db.MetaData()

        emp = db.Table(parser, metadata,
              db.Column('Id', db.Integer()),
              db.Column('Date', db.BigInteger() , nullable=False),
              db.Column('Data', db.String()),
              )

        metadata.create_all(cortex_db)

        query = db.insert(emp).values(Id=int(user_id), Date=(time), Data=data) 
        ResultProxy = connection.execute(query)

    @saver('file_data')
    def raw_data_saver(parser, user_id, time, data, msgQueue, cortex_db):

        msgQueue.add_queue('filedata')

        connection = cortex_db.connect()
        metadata = db.MetaData()

        emp = db.Table(parser, metadata,
              db.Column('Id', db.Integer()),
              db.Column('Date', db.BigInteger() , nullable=False),
              db.Column('Path', db.String()),
              )

        metadata.create_all(cortex_db)

        query = db.insert(emp).values(Id=int(user_id), Date=(time), Path=data) 
        ResultProxy = connection.execute(query)

    return savers