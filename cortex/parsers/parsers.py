import json

from .parsers import *

parsers = dict()

def parser(name):
    def decorator(f):
        def callback(ch, method, properties, body):
            print(f" [x] Received {body} parser: {name} ")
            ch.basic_ack(delivery_tag = method.delivery_tag)

        parsers[name] = callback
    return decorator
    
@parser('pose')
def parse_pose(context, snapshot):
    pose_json = json.dumps(dict(
        px = snapshot.pose.translation.x,
        py = snapshot.pose.translation.y,
        pz = snapshot.pose.translation.z,

        rx = snapshot.pose.Rotation.x,
        ry = snapshot.pose.Rotation.y,
        rz = snapshot.pose.Rotation.z,
        rw = snapshot.pose.Rotation.w
        ))
 
    fname = f'pose_{snapshot.datetime}.json'
    context.save(fname, pose_json)
    return fname

@parser('color_image')
def parse_color_image(context, snapshot):
    pose_json = json.dumps(dict(
        px = snapshot.pose.translation.x,
        py = snapshot.pose.translation.y,
        pz = snapshot.pose.translation.z,

        rx = snapshot.pose.Rotation.x,
        ry = snapshot.pose.Rotation.y,
        rz = snapshot.pose.Rotation.z,
        rw = snapshot.pose.Rotation.w
        ))
 
    fname = f'pose_{snapshot.datetime}.json'
    context.save(fname, pose_json)
    return fname