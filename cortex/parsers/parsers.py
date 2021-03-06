import json
from pathlib import Path
from PIL import Image
import struct 
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import shutil


from .. import PoseMsg
from .. import ColorImageMsg
from .. import DepthImageMsg
from .. import FeelingsMsg
from .. import MsgQueue


all_parsers = dict()

def parser(name):
    """
    Decorates and adds the parsers to a global dictionary
    """
    def decorator(parse_function):
        all_parsers[name] = parse_function
        return parse_function
    return decorator

def run_parser(name, queue_url ):
    """
    Runs <name> parsers that work with <queue_url> queue.
    """
    print (f'Parser {name} starting...')
    msgQueue = MsgQueue(queue_url)

    parsers = queue_parser_factory(msgQueue)

    msgQueue.add_exchange('parsers', 'fanout')
    for key in parsers.keys():
        msgQueue.bind_exchange('parsers', key)

    msgQueue.add_consumer(name, parsers[name])
    msgQueue.consume()

def parse(name, data):
    """
    Return parse the <data> with <name> parser and returns the result.
    """
    return all_parsers[name](data)
        
@parser('pose')
def parse_pose(data):
    """
    Parses protobuf pose
    """ 
    pose = PoseMsg()
    pose.ParseFromString(data)

    pose_json = json.dumps(dict(
            px = pose.translation.x,
            py = pose.translation.y,
            pz = pose.translation.z,
            rx = pose.rotation.x,
            ry = pose.rotation.y,
            rz = pose.rotation.z,
            rw = pose.rotation.w
            ))
    return pose_json
         

@parser('color_image')
def parse_color_image(data):
    """
    Parses protobuf color_image
    """ 
    color_image = ColorImageMsg()
    color_image.ParseFromString(data)

    image = Image.frombytes('RGB', (color_image.width, color_image.height), color_image.data, 'raw')

    tmp_file = tempfile.NamedTemporaryFile()                
    path_str = tmp_file.name
    tmp_file.close()

    image.save(path_str, 'png')
    return path_str

@parser('depth_image')
def parse_depth_image(data):
    """
    Parses protobuf depth_image
    """ 
    depth_image = DepthImageMsg()
    depth_image.ParseFromString(data)

    #Format to byte array as np image can eats

    special_prefix_array = [bytearray()]
    special_prefix_array.extend(depth_image.data)
    data_bytearray = bytes(reduce(lambda a, x: a + bytearray(struct.pack('d', x)), special_prefix_array))
    array_np = np.frombuffer(data_bytearray).reshape((depth_image.height, depth_image.width))

    plt.imshow(array_np, cmap='binary', interpolation='nearest')

    plt.axis('off')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    tmp_file = tempfile.NamedTemporaryFile()                
    path_str = tmp_file.name +'.png'
    tmp_file.close()
            
    plt.savefig(path_str)
    return path_str 
         


@parser('feelings')
def parse_feelings(data):
    """
    Parses protobuf feelings
    """ 

    feelings = FeelingsMsg()
    feelings.ParseFromString(data)

    feelings_json = json.dumps(dict(
        hunger = feelings.hunger,
        thirst = feelings.thirst,
        exhaustion = feelings.exhaustion,
        happiness = feelings.happiness
        ))

    return feelings_json
        

def queue_parser_factory(msgQueue):
    """
    Returns a dictionary with all the pasrers. 
    Uses decoration in order create appropriate from simpler functions/ 
    """

    def queue_parser(name, msgQueue):
        def callback(ch, method, properties, body):

            suffix, time = body.decode("utf-8").split(":")
            path = Path(suffix) / name / time


            if (general_wrapper(name, path, msgQueue)):
                ch.basic_ack(delivery_tag = method.delivery_tag)


        return callback
        

    def general_wrapper(name, path, queue):
        try:
            msgQueue.add_queue('raw_data')

            #If the file is not available continue
            try:
                data = path.read_bytes()
            except Exception as e:
                return True

            result = parse(name, data)

            if 'image' in name:
                
                path_str = str(path) + '.png'

                shutil.move(result, path_str)

                msgQueue.publish(ex_name='',q_name='raw_data', msg=str(path)+":"+path_str)
            else:
                msgQueue.publish(ex_name='',q_name='raw_data', msg=str(path)+":"+result)
       
            
            path.unlink()

            return True
        except Exception as e:
            print (e)
            return False

    parsers = dict()


    for parser in all_parsers.keys():
        parsers[parser] = queue_parser(parser, msgQueue)

    

    return parsers