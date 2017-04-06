#!/usr/bin/env python 
import roslib
from gazebo_msgs.srv import*
import rospy

def gms_client(model_name, relative_entity_name):
	rospy.wait_for_service('/gazebo/get_model_state')
	try:
		gms = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
		resp1 = gms(model_name,relative_entity_name)
		return resp1
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

if __name__ == "__main__":
	rospy.init_node('test_node')
	rate = rospy.Rate(20.0)
	while not rospy.is_shutdown():
		res = gms_client('atrv','world')
		print res.pose.position
		rate.sleep()

