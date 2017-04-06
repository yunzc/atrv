#!/usr/bin/env python  
import roslib
import rospy
import math
import tf


if __name__ == '__main__':
    rospy.init_node('tf_listener')
    print("WTHuck")
    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        print('trying...')
        try:
            (trans,rot) = listener.lookupTransform('map', 'vicon/ATRV_1/ATRV_1', rospy.Time(0))
            print(trans)
            print(rot)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("FAIL")
            continue

        rate.sleep()
