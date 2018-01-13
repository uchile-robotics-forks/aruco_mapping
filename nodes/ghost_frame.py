#!/usr/bin/env python  
import roslib
import rospy

import tf

if __name__ == '__main__':
    rospy.init_node('ghost_frame_spawner')  
    listener = tf.TransformListener()
    br = tf.TransformBroadcaster()
    #listener.waitForTransform('odom','base_footprint',rospy.Time.now(),rospy.Duration(3.0))
    while True :
        try :
            (trans,rot) = listener.lookupTransform('odom', 'base_footprint', rospy.Time(0))
            break
        except:
            rospy.logerr('not transform between odom and base_footprint')
            continue
    rate = rospy.Rate(100.0)
    while not rospy.is_shutdown() and len(trans)!=0:
        br.sendTransform(trans,rot,rospy.Time.now(),'base_map','odom')
        rate.sleep()