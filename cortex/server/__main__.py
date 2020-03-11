import sys
import click

from pathlib import Path
from .server import Handler
from .listener import Listener


@click.command()
@click.option('--host', default="127.0.0.1", help='server\'s ip')
@click.option('--port', default=8000, help='server\'s port')
@click.option('--queue_url', default='rabbitmq://127.0.0.1:5672/', help='url of the message queue')
@click.option('--root', default='~', help='root directory for files')
def run(host, port, queue_url, root):
    """
    Listen to incoming client connections, parse them and prints the msg
    """
    server = Listener(host, port)
    
    server.start()

    

    while (1):  
        client = server.accept()
        handler = Handler(client, root, queue_url)
        handler.start()
          
    server.stop()


if __name__ == '__main__':
    run()
