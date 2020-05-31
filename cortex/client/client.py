from .. import UserMsg
from .. import SnapshotMsg
from .. import Connection
import sys
import gzip
import struct


def upload_sample(host, port, path, encoding='gz', formating='proto'):
    """
    Read raw data zipped flie from <path>.
    Send user information and snapshots serialized to server
    Write now only proto_buf formater is supported, it does almost nothing.
    Future formaters will read the data into proto_buf structure and send it that way.
    """

    print ("Client starting...")
    try:
        reader = getReader(path, encoding)

        with Connection.connect(host, int(port)) as conn:
            with reader as raw_data:


                send_user_data(conn, raw_data, formating)

                try:
                    while 1:
                        if send_snapshot(conn, raw_data, formating) == False:
                            break
                except:
                    return 
    except Exception as e:
        print(e)


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