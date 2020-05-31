import click
from pathlib import Path
from .. import MsgQueue
from .saver import run_saver as run_saver_imp
from .saver import save as save_imp

@click.group()
def cli():
    pass

@click.command()
@click.argument('db_url', nargs=1, default='postgresql://127.0.0.1:5432/', type=click.UNPROCESSED)
@click.argument('queue_url', nargs=1, default='rabbitmq://127.0.0.1:5672/', type=click.UNPROCESSED)
def run_saver(db_url, queue_url):
     
    run_saver_imp(db_url, queue_url)

@click.command()
@click.option('-d', '--database', default='postgresql://127.0.0.1:5432/', help='database to save the information to')
@click.argument('parser', nargs=1, required=True, type=click.UNPROCESSED)
@click.argument('data_file', nargs=1, required=True, type=click.UNPROCESSED)
def save(database, parser, data_file):
     
    try:
        path = Path(data_file)

        data = path.read_bytes()
    except:
        print ("Error reading file: "+data_file)
        return

    save_imp(database, parser, data)
       

if __name__ == '__main__':
    cli.add_command(run_saver)
    cli.add_command(save)
    cli()
