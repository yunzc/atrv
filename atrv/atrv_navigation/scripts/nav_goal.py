#!/usr/bin/python

import roslib
import rospy
#import simple action client
import actionlib
#imports messages used by move_base_msgs
import move_base_msgs.msg
from geometry_msgs.msg import PoseWithCovarianceStamped

def nav_goal_client(goal, client, goal_x, goal_y, goal_w):
	goal.target_pose.header.stamp = rospy.get_rostime()
	goal.target_pose.pose.position.x = goal_x
	goal.target_pose.pose.position.y = goal_y
	goal.target_pose.pose.orientation.w = goal_w
	#sends goal to action server
	client.send_goal(goal)
	#waits for the server to finish performing action
	client.wait_for_result()
	return client.get_result()

def nav():
    client=actionlib.SimpleActionClient("move_base",move_base_msgs.msg.MoveBaseAction)
    client.wait_for_server()
    #creates goal to send to action server
    goal=move_base_msgs.msg.MoveBaseGoal()
    goal.target_pose.header.frame_id = "vicon_origin"
    print "current frame: ", goal.target_pose.header.frame_id
    x = float(input("x coordinate: "))
    y = float(input("y coordinate: "))
    w = float(input("orientation: "))
    result = nav_goal_client(goal, client, x, y, w)
    print "updated position"
    return True

if __name__ == '__main__':
	try:
		rospy.init_node('nav_goal')
		task = nav()
		print "arrived!"

	except rospy.ROSInterruptException:
		print "program interrupted before completion"
