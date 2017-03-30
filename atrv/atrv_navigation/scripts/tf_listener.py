#!/usr/bin/env python  
import roslib
import rospy
import math
import tf


if __name__ == '__main__':
    rospy.init_node('tf_listener')

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('odom', 'base_link', rospy.Time(0))
            print(trans)
            # print(rot)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("FAIL")
            continue

        rate.sleep()
