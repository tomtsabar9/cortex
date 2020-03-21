import click
import sqlalchemy as db
from .. import MsgQueue

from .saver import *

@click.command()
@click.option('--db-url', default='postgresql://postgres:mysecretpassword@172.17.0.3:5432/', help='db url')
@click.option('--queue_url', default='rabbitmq://127.0.0.1:5672/', help='queue url')
def run_saver(db_url, queue_url):
     
    msgQueue = MsgQueue(queue_url)

    cortex_db = db.create_engine(db_url)
    savers = saver_factory()

    #Inject msqQueue
    savers['queue'] = msgQueue

    #Inject DB
    savers['db'] = cortex_db

    for key in savers.keys():
        if key not in ['queue', 'db']:
            msgQueue.add_consumer(key, savers[key])
            msgQueue.consume()

if __name__ == '__main__':
    run_saver()
