import sys
import click
from .gui import run

@click.command()
@click.option('--host', default="127.0.0.1", help='server\'s ip')
@click.option('--port', default=8080, help='server\'s port')
@click.option('--api-host', default="127.0.0.1", help='api\'s ip')
@click.option('--api-port', default=5000, help='api\'s port')
def run_server(host, port, api_host, api_port):
    """
    
    """
    run(host, port, api_host, api_port)

 
if __name__ == '__main__':
    run_server()