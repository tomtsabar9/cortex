from .. import UserMsg
from .. import SnapshotMsg
from .. import Connection
import sys
import gzip
import struct
import click

def send_serialized_data(conn, data_stream):
    """
    Gets connection and datastream.
    Reads serialized user data from stream and send to connection/
    """

    try:
        size = struct.unpack('<I', data_stream.read(4))[0]  
        user_raw_data = data_stream.read(size)
    
        conn.send(user_raw_data)
        return True
    except Exception as e:
        print (e)
        return False
    

def send_user_data(conn, data_stream):
    """
    stub for readibilty, see send_serialized_data
    """
    return send_serialized_data(conn, data_stream)

def send_snapshot(conn, data_stream):
    """
    stub for readibilty, see send_serialized_data
    """
    return send_serialized_data(conn, data_stream)



@click.command()
@click.option('--host', default="127.0.0.1", help='server\'s ip')
@click.option('--port', default=8000, help='server\'s port')
@click.option('--path', default="sample.mind.gz", help='path to data file')
def upload_sample(host, port, path):
    """
    Read raw data zipped flie from <path>.
    Send user information and snapshots serialized to server
    """

    with Connection.connect(host, int(port)) as conn:
        with gzip.open(path,'rb') as raw_data:


            send_user_data(conn, raw_data)

            while 1:
                if send_snapshot(conn, raw_data) == False:
                    break

            
    print("done")

if __name__ == '__main__':
    upload_sample()

