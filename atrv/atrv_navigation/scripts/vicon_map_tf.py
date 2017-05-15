#!/usr/bin/env python
import rospy
import tf
import tf2_ros
import geometry_msgs.msg

"""
Publishing a static transform to account for the offset between the vicon origin and the map origin 
and then a static transform between the vicon atrv and base link for any small offsets
The parameters assigned below should be the transformation from map to vicon
(where the map origin is with respect to the vicon origin)
"""
# parameters for the map:
# parent = "/vicon_origin"
# child = "map"
map_x = 1
map_y = 1
map_z = 1
map_yaw = 0
map_pitch = 0
map_roll = 0

# parameters for atrv-baselink
# parent = "vicon/ATRV_1/ATRV_1"
# child = "baselink"
atrv_x = 0
atrv_y = 0
atrv_z = 0
atrv_yaw = 0
atrv_pitch = 0
atrv_roll = 0

def handlePose(stBroadcaster, parent, child, x, y, z, yaw, pitch, roll):
    static_transformStamped = geometry_msgs.msg.TransformStamped()

    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = parent
    static_transformStamped.child_frame_id = child

    static_transformStamped.transform.translation.x = x
    static_transformStamped.transform.translation.y = y
    static_transformStamped.transform.translation.z = z

    quat = tf.transformations.quaternion_from_euler(yaw, pitch, roll)
    static_transformStamped.transform.rotation.x = quat[0]
    static_transformStamped.transform.rotation.y = quat[1]
    static_transformStamped.transform.rotation.z = quat[2]
    static_transformStamped.transform.rotation.w = quat[3]

    STbroadcaster.sendTransform(static_transformStamped)

if __name__ == '__main__':
    # initialize node
    rospy.init_node('vicon_map_tf')
    # initialize transform broadcaster
    STbroadcaster = tf2_ros.StaticTransformBroadcaster()

    rate = rospy.Rate(20.0)
    while not rospy.is_shutdown():
        # static transform btwn map and vicon
        handlePose(STbroadcaster, "/vicon_origin", "map", map_x, map_y, map_z, map_yaw, map_pitch, map_roll)
        rate.sleep()
