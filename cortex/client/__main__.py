import click
from .client import upload_sample as upload_sample_imp

@click.group()
def cli():
    pass

@click.command()
@click.option('-h', '--host', default='127.0.0.1', help='server\'s ip')
@click.option('-p', '--port', default=8000, help='server\'s port')
@click.option('--encoding', default='gz', help='encoding type')
@click.option('--formating', default='proto', help='formating type')
@click.argument('path', nargs=1, default='sample.mind.gz', type=click.UNPROCESSED)
def upload_sample(host, port,encoding, formating, path):
    """
    Read raw data from <path>. Send user information and snapshots serialized to server.
    """

    upload_sample_imp(host, port, path, encoding, formating)
            
    print('done')

if __name__ == '__main__':
    cli.add_command(upload_sample)
    cli()

