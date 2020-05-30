import pika
import click
from pathlib import Path

from .parsers import run_parser as run_parser_imp
from .parsers import parse as parse_imp
from .. import MsgQueue

@click.group()
def cli():
    pass

@click.command()
@click.argument('name', nargs=1, required=True, type=click.UNPROCESSED)
@click.argument('queue_url', nargs=1, default='rabbitmq://127.0.0.1:5672/', type=click.UNPROCESSED)
def run_parser(name, queue_url):
     
    run_parser_imp(name, queue_url=queue_url)

@click.command()
@click.argument('name', nargs=1, required=True, type=click.UNPROCESSED)
@click.argument('data_file', nargs=1, type=click.UNPROCESSED)
def parse(name, data_file):

    try:
        path = Path(data_file)

        data = path.read_bytes()
    except:
        print ("Error reading file: "+data_file)
        return
     
    print (parse_imp(name, data))

if __name__ == '__main__':
    cli.add_command(run_parser)
    cli.add_command(parse)
    cli()