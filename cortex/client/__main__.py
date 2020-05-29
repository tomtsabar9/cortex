import click
from .client import upload_sample

@click.command()
@click.option('--host', default="127.0.0.1", help='server\'s ip')
@click.option('--port', default=8000, help='server\'s port')
@click.option('--path', default="sample.mind.gz", help='path to data file')
@click.option('--encoding', default="gz", help='encoding type')
@click.option('--formating', default="proto", help='formating type')
def upload(host, port, path, encoding, formating):
    """
    Read raw data zipped flie from <path>.
    Send user information and snapshots serialized to server
    """

    upload_sample(host, port, path, encoding, formating)

            
    print("done")

if __name__ == '__main__':
    upload()

