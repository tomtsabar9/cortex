from .. import UserMsg
from .. import SnapshotMsg
from .. import Connection
import sys
import gzip
import struct
import click

def send_serialized_data(conn, data_stream, formater):
    """
    Gets connection and datastream.
    Reads serialized user data from stream and send to connection/
    """


    try:
        conn.send(formater(data_stream))
        return True
    except Exception as e:
        print (e)
        return False
    

def proto_formater(data_stream):
    size = struct.unpack('<I', data_stream.read(4))[0]  
    return data_stream.read(size)

def default_formater(data_stream):
    return proto_formater

def send_user_data(conn, data_stream, formating):
    """
    stub for readibilty and future differences between send_user_data and send_snapshot
    """

    if formating == "proto":
        return send_serialized_data(conn, data_stream, proto_formater)

    return send_serialized_data(conn, data_stream, default_formater)

def send_snapshot(conn, data_stream, formating):
    """
    stub for readibilty and future differences between send_user_data and send_snapshot
    """
    if formating == "proto":
        return send_serialized_data(conn, data_stream, proto_formater)

    return send_serialized_data(conn, data_stream, default_formater)
def getReader(path, encoding):
    if encoding == 'gz':
        return gzip.open(path,'rb')

    return open(path, 'rb')

@click.command()
@click.option('--host', default="127.0.0.1", help='server\'s ip')
@click.option('--port', default=8000, help='server\'s port')
@click.option('--path', default="sample.mind.gz", help='path to data file')
@click.option('--encoding', default="gz", help='encoding type')
@click.option('--formating', default="proto", help='formating type')

def upload_sample(host, port, path, encoding, formating):
    """
    Read raw data zipped flie from <path>.
    Send user information and snapshots serialized to server
    """

    reader = getReader(path, encoding)

    with Connection.connect(host, int(port)) as conn:
        with reader as raw_data:


            send_user_data(conn, raw_data, formating)

            while 1:
                if send_snapshot(conn, raw_data, formating) == False:
                    break

            
    print("done")

if __name__ == '__main__':
    upload_sample()

