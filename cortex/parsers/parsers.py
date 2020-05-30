import json
from pathlib import Path
from PIL import Image
import struct 
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

from .. import PoseMsg
from .. import ColorImageMsg
from .. import DepthImageMsg
from .. import FeelingsMsg
from .. import MsgQueue


def parser_factory():
    """
    Returns a dictionary with all the pasrers. 
    Uses decoration in order create appropriate from simpler functions/ 
    """
    parsers = dict()

    def parser(name):
        def decorator(parse_function):
            def callback(ch, method, properties, body):

                suffix, time = body.decode("utf-8").split(":")
                path = Path(suffix) / name / time

                if (parse_function(path, parsers["queue"])):
                    ch.basic_ack(delivery_tag = method.delivery_tag)

            parsers[name] = callback
            parsers[name+'_orig'] = parse_function

        return decorator
        
    @parser('pose')
    def parse_pose(path, msgQueue):

        msgQueue.add_queue('raw_data')

        try:
            pose = PoseMsg()
            pose.ParseFromString(path.read_bytes())

            pose_json = json.dumps(dict(
                px = pose.translation.x,
                py = pose.translation.y,
                pz = pose.translation.z,
                rx = pose.rotation.x,
                ry = pose.rotation.y,
                rz = pose.rotation.z,
                rw = pose.rotation.w
                ))
         
            print (str(path)+":"+pose_json)
            msgQueue.publish(ex_name='',q_name='raw_data', msg=str(path)+":"+pose_json)

            path.unlink()

            return True
        except Exception as e:
            print (e)
            return False

    @parser('color_image')
    def parse_color_image(path, msgQueue):
        
        msgQueue.add_queue('raw_data')

        try:
            color_image = ColorImageMsg()
            color_image.ParseFromString(path.read_bytes())

            image = Image.frombytes("RGB", (color_image.width, color_image.height), color_image.data, 'raw')

            path.unlink()

            path_str = str(path) + '.png'
            image.save(path_str, 'png')
         
            msgQueue.publish(ex_name='',q_name='raw_data', msg=str(path)+":"+path_str)

            return True
        except Exception as e:
            print (e)
            return False

    @parser('depth_image')
    def parse_depth_image(path, msgQueue):
        msgQueue.add_queue('raw_data')

        try:
            depth_image = DepthImageMsg()
            depth_image.ParseFromString(path.read_bytes())


            #Format to byte array as np image can eats

            special_prefix_array = [bytearray()]
            special_prefix_array.extend(depth_image.data)
            data_bytearray = bytes(reduce(lambda a, x: a + bytearray(struct.pack("d", x)), special_prefix_array))
            array_np = np.frombuffer(data_bytearray).reshape((depth_image.height, depth_image.width))

            plt.imshow(array_np, cmap='binary', interpolation='nearest')

            plt.axis('off')
            plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

            path.unlink()
            
            path_str = str(path) + '.png'
            plt.savefig( path_str) 
         
            msgQueue.publish(ex_name='',q_name='raw_data', msg=str(path)+":"+path_str)

            return True
        except Exception as e:
            print (e)
            return False

    @parser('feelings')
    def parse_feelings(path, msgQueue):

        msgQueue.add_queue('raw_data')

        try:
            feelings = FeelingsMsg()
            feelings.ParseFromString(path.read_bytes())

            feelings_json = json.dumps(dict(
                hunger = feelings.hunger,
                thirst = feelings.thirst,
                exhaustion = feelings.exhaustion,
                happiness = feelings.happiness
                ))
         
            msgQueue.publish(ex_name='',q_name='raw_data', msg=str(path)+":"+feelings_json)

            path.unlink()

            return True
        except Exception as e:
            print (e)
            return False

    return parsers