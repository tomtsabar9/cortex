from .. import UserMsg
from .. import SnapshotMsg
from .. import Connection
import sys
import gzip
import struct

def upload_sample(host, port, path):
    """
    TODO
    """

    with Connection.connect(host, int(port)) as conn:
        with gzip.open(path,'rb') as raw_data:

            userMsg = UserMsg()

            size = struct.unpack('<I', raw_data.read(4))[0]  
            user_raw_data = raw_data.read(size)
            
            userMsg.ParseFromString(user_raw_data)
        
            conn.send(userMsg.SerializeToString())


    print("done")

def main(argv):
    if len(argv) != 4:
        print(f'TODO')
        return 1

    upload_sample(argv[1], argv[2], argv[3])

if __name__ == '__main__':
    main(sys.argv)

