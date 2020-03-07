
import json

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
 
    print (pose_json)
    context.save('translation.json', pose_json)
