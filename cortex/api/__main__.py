import sys
import click
from .api import create_api


@click.command()
@click.option('--host', default="127.0.0.1", help='server\'s ip')
@click.option('--port', default=5000, help='server\'s port')
@click.option('--db-url', default='postgresql://postgres:mysecretpassword@127.0.0.1:5432/', help='db url')
def run_api(host, port, db_url):
    """
    Read raw data zipped flie from <path>.
    Send user information and snapshots serialized to server
    """


    api = create_api(db_url)  
    api.run()

if __name__ == '__main__':
    run_api()