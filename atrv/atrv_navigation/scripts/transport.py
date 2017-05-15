#!/usr/bin/python

import roslib
import rospy
#import simple action client
import actionlib
#imports messages used by move_base_msgs
import move_base_msgs.msg
from geometry_msgs.msg import TransformStamped
import time

list_of_fun = ['redblock_small', 'glove1', 'wambase']

# Input "loki" or "baxter" then the atrv will navigate to it
class atrv_navigation():
	# This class is for use of navigating the atrv using a simpla action client
	# with ros move_base to navigate the atrv to a particular goal
	def __init__(self, frame='vicon_origin', object_list=list_of_fun):
		rospy.init_node('atrv_transport')
		self.object_list = object_list
		self.client = actionlib.SimpleActionClient("move_base",move_base_msgs.msg.MoveBaseAction)
		#### note that server will only go on when you have a move_base running
		self.client.wait_for_server()
		self.goal = move_base_msgs.msg.MoveBaseGoal()
		self.goal.target_pose.header.frame_id = frame
		print "current frame: ", self.goal.target_pose.header.frame_id
		self.desired_goal = None
		self.prev_goal = None
		self.quit = False
		self.sub = None

	def nav_goal_client(self):
		if self.desired_goal != None: # as a safety measure
			self.goal.target_pose.header.stamp = rospy.get_rostime()
			self.goal.target_pose.pose.position.x = self.desired_goal[0]
			self.goal.target_pose.pose.position.y = self.desired_goal[1]
			self.goal.target_pose.pose.orientation.w = self.desired_goal[2]
			#sends goal to action server
			self.client.send_goal(self.goal)
			#waits for the server to finish performing action
			self.client.wait_for_result()
			return self.client.get_result()

	def get_vicon_obj(self, msg, epsilon=0.2):
		incoming_goal = [msg.transform.translation.x, msg.transform.translation.y, 1.0]
		# rotation shouldn't be dictated: should be the easiest orientation
		if self.prev_goal == None:
			self.desired_goal = incoming_goal
		else:
			if abs(incoming_goal[0]-self.prev_goal[0]) > epsilon or abs(incoming_goal[1]-self.prev_goal[1]) > epsilon:
				self.desired_goal = incoming_goal
			else:
				self.desired_goal = None

	def get_goal_pose(self, friend):
		# friend input should be small_red, loki, or glove for now
		if friend not in self.object_list:
			self.quit = True
			return False
		rostop = '/vicon/'+friend+'/'+friend
		if(self.sub):
			self.sub.unregister()
		self.sub = rospy.Subscriber(rostop, TransformStamped, self.get_vicon_obj, queue_size=1)
		return True

	def nav(self):
		result = self.nav_goal_client()
		print "updated position"
		self.desired_goal = None
		return True

	def run(self):
		while not self.quit:
			try:
				objj = raw_input('enter object (redblock_small, glove1, or wambase): ')
				getpose = self.get_goal_pose(objj)
				if not getpose:
					print("program terminated")
					return True
				tolerance = 10
				while self.desired_goal == None:
					time.sleep(0.5)
					tolerance -= 1
					if tolerance == 0:
						print('callback timeout')
						return True
				print(self.desired_goal)
				self.nav()
				self.prev_goal = self.desired_goal
				self.desired_goal = None
			except rospy.ROSInterruptException:
				print("program terminated")
				return True


if __name__ == '__main__':
	att = atrv_navigation()
	print("created")
	att.run()
