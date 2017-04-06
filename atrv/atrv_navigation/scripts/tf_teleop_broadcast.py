#!/usr/bin/env python  
import roslib
import rospy
import tf
from gazebo_msgs.srv import*

def getModelPose(link_name='base_link', relative_entity_name='world'):
    rospy.wait_for_service('/gazebo/get_link_state')
    try:
        gls = rospy.ServiceProxy('gazebo/get_link_state', GetLinkState)
        resp = gls(link_name,relative_entity_name)
        return resp
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def handleModelPose(msg, tfBroadcaster, tfListener, linkname="base_link", framename="vicon/ATRV_1/ATRV_1"):
    position = msg.link_state.pose.position
    ori = msg.link_state.pose.orientation
    # link is child frame is parent
    tfBroadcaster.sendTransform(
                    (position.x, position.y, position.z),
                    (ori.x, ori.y, ori.z, ori.w),
                    rospy.Time.now(),
                    linkname,
                    framename)

if __name__ == '__main__':
    rospy.init_node('atrv_tf_broadcaster')
    br = tf.TransformBroadcaster()
    ls = tf.TransformListener()
    rate = rospy.Rate(20.0)
    while not rospy.is_shutdown():
        msg = getModelPose()
        try: 
            handleModelPose(msg, br, ls)
        except:
            pass
        rate.sleep()