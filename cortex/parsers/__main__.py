import pika
import click

from .parsers import *
from .. import MsgQueue

@click.command()
@click.option('--name', required=True, help='consumer type')
@click.option('--queue_url', default='rabbitmq://127.0.0.1:5672/', help='server\'s port')
def run_parser(name, queue_url):
    global parsers
    msgQueue = MsgQueue(queue_url)

    #Inject msqQueue
    parsers["queue"] = msgQueue

    msgQueue.add_consumer(name, parsers[name])
    msgQueue.consume()

if __name__ == '__main__':
    run_parser()