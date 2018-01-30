#!/usr/bin/env python  
import roslib
import rospy
import sys

import tf

if __name__ == '__main__':
    ghost_frame_name = sys.argv[1]
    rospy.init_node(ghost_frame_name+'_frame_spawner')  
    listener = tf.TransformListener()
    br = tf.TransformBroadcaster()
    #listener.waitForTransform('odom','base_footprint',rospy.Time.now(),rospy.Duration(3.0))
    listener.waitForTransform('odom','camera_orb_position',rospy.Time(0),rospy.Duration(3.0))
    while not rospy.is_shutdown() :
        try :
            (trans,rot) = listener.lookupTransform('odom', 'camera_orb_position', rospy.Time(0))
            rospy.loginfo("transform ok")
            break
        except:
            rospy.logerr('not transform between odom and base_footprint')
            continue
    rate = rospy.Rate(100.0)
    while not rospy.is_shutdown() and len(trans)!=0:
        br.sendTransform(trans,rot,rospy.Time.now(),ghost_frame_name,'odom')
        rate.sleep()