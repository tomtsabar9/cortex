import sys
import click
from .gui import run_server as run_server_imp

@click.group()
def cli():
    pass

@click.command()
@click.option('-h', '--host', default="127.0.0.1", help='server\'s ip')
@click.option('-p', '--port', default=8080, help='server\'s port')
@click.option('-H', '--api-host', default="127.0.0.1", help='api\'s ip')
@click.option('-P', '--api-port', default=5000, help='api\'s port')
def run_server(host, port, api_host, api_port):
    """
    
    """
    run_server_imp(host, port, api_host, api_port, cli=True)

 
if __name__ == '__main__':
    cli.add_command(run_server)
    cli()