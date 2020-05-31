import sys
import click
from .api import run_api_server

@click.group()
def cli():
    pass


@click.command()
@click.option('-h', '--host', default="127.0.0.1", help='server\'s ip')
@click.option('-p', '--port', default=5000, help='server\'s port')
@click.option('-d','--database', default='postgresql://127.0.0.1:5432/', help='db url')
def run_server(host, port, database):
    """
    Cli that runs the api server
    """
    run_api_server(host, port, database, cli=True)
    

if __name__ == '__main__':
    cli.add_command(run_server)
    cli()