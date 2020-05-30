import sys
import click

from pathlib import Path
from .server import run_server as run_server_imp
import signal

handlers = []

def signal_handler(sig, frame):
    print('Exiting...')
    for hanlder in handlers:
        hanlder.stop() 
        hanlder.join() 
    print('Finished')
    sys.exit(0)

@click.group()
def cli():
    signal.signal(signal.SIGINT, signal_handler)

@click.command()
@click.option('-h', '--host', default="127.0.0.1", help='server\'s ip')
@click.option('-p', '--port', default=8000, help='server\'s port')
@click.option('-r', '--root', default='data', help='root directory for files')
@click.argument('queue_url', nargs=1, default='rabbitmq://127.0.0.1:5672/', type=click.UNPROCESSED)
def run_server(host, port, root, queue_url):
    """
    Listen to incoming client connections, parse them and prints the msg
    """
    signal.signal(signal.SIGINT, signal_handler)
    run_server_imp(host, port, queue_url, root, handlers = handlers)

          
    server.stop()


if __name__ == '__main__':
    cli.add_command(run_server)
    cli()
