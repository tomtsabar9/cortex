import pika
import click

from .parsers import *
from .. import MsgQueue

@click.group()
def cli():
    pass

@click.command()
@click.argument('name', nargs=1, required=True, type=click.UNPROCESSED)
@click.argument('queue_url', nargs=1, default='rabbitmq://127.0.0.1:5672/', type=click.UNPROCESSED)
def run_parser(name, queue_url):
     
    msgQueue = MsgQueue(queue_url)

    parsers = parser_factory()
    #Inject msqQueue
    parsers["queue"] = msgQueue

    msgQueue.add_exchange('parsers', 'fanout')
    for key in parsers.keys():
        if 'orig' in key:
            continue
        msgQueue.bind_exchange('parsers', key)

    msgQueue.add_consumer(name, parsers[name])
    msgQueue.consume()

if __name__ == '__main__':
    cli.add_command(run_parser)
    cli()