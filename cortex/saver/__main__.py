import click
import sqlalchemy as db
import threading

from .. import MsgQueue

from .saver import *

@click.command()
@click.option('--db-url', default='postgresql://postgres:mysecretpassword@127.0.0.1:5432/', help='db url')
@click.option('--queue_url', default='rabbitmq://127.0.0.1:5672/', help='queue url')
def run_saver(db_url, queue_url):
     
    msgQueue = MsgQueue(queue_url)

    cortex_db = db.create_engine(db_url)
    savers = saver_factory()


    #Inject msqQueue
    savers['queue'] = msgQueue

    #Inject DB
    savers['db'] = cortex_db


    msgQueue.add_consumer('raw_data', savers['raw_data'])
    msgQueue.consume()
       

if __name__ == '__main__':
    run_saver()
