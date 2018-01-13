#!/usr/bin/env python  
import roslib
import rospy
import numpy
import tf

if __name__ == '__main__':
    rospy.init_node('localization_based_on_aruco')  
    listener = tf.TransformListener()
    transformer_ros = tf.TransformerROS()
    br = tf.TransformBroadcaster()
    listener.waitForTransform('map','camera_position',rospy.Time(0),rospy.Duration(3.0))
    rate = rospy.Rate(150.0)
    while not rospy.is_shutdown():
        (trans_mc,rot_mc) = listener.lookupTransform('map', 'camera_position', rospy.Time(0))
        (trans_co,rot_co) = listener.lookupTransform('CameraTop_optical_frame', 'odom',rospy.Time(0))
        # translations = zip(trans_mc,trans_oc)
        # trans=tuple(map(sum,translations))
        # print trans
        matrix_mc =transformer_ros.fromTranslationRotation(trans_mc,rot_mc)
        matrix_co =transformer_ros.fromTranslationRotation(trans_co,rot_co)
        matrix_mo=numpy.dot(matrix_mc,matrix_oc)
        scale, shear, angles, trans, persp = tf.transformations.decompose_matrix(matrix_mo)
        rot=tf.transformations.quaternion_from_euler(*angles)
        # matrix_mc = tf.transformations.quaternion_matrix(rot_mc)
        # matrix_oc = tf.transformations.quaternion_matrix(rot_oc)
        # matrix_rot = tf.transformations.concatenate_matrices(matrix_mc,matrix_oc)
        #rot = tf.transformations.quaternion_from_matrix(matrix_rot)
        br.sendTransform(trans,rot,rospy.Time.now(),'odom','map')
        rate.sleep()
