#!/usr/bin/env python
import rospy
import tf
import tf2_ros
import geometry_msgs.msg

"""
Publishing a static transform to accoutn for the offset between the vicon origin and the mapp origin 
The parameters assigned below should be the transformation from map to vicon
(where the map origin is with respect to the vicon origin)
"""
map_x = 1
map_y = 1
map_z = 1
map_yaw = 0
map_pitch = 0
map_roll = 0


if __name__ == '__main__':
    # initialize node   
    rospy.init_node('vicon_map_tf')
    # initialize transform broadcaster 
    broadcaster = tf2_ros.StaticTransformBroadcaster()

    static_transformStamped = geometry_msgs.msg.TransformStamped()
  
    static_transformStamped.header.stamp = rospy.Time.now()
    static_transformStamped.header.frame_id = "/vicon_origin"
    static_transformStamped.child_frame_id = "map"
  
    static_transformStamped.transform.translation.x = map_x
    static_transformStamped.transform.translation.y = map_y
    static_transformStamped.transform.translation.z = map_z
  
    quat = tf.transformations.quaternion_from_euler(map_yaw, map_pitch, map_roll)
    static_transformStamped.transform.rotation.x = quat[0]
    static_transformStamped.transform.rotation.y = quat[1]
    static_transformStamped.transform.rotation.z = quat[2]
    static_transformStamped.transform.rotation.w = quat[3]
 
    broadcaster.sendTransform(static_transformStamped)
    rospy.spin()