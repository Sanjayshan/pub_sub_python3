#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

def call_set_pen_service(r,g,b,width,off):
     try:
          pass
          set_pen=rospy.ServiceProxy("/turtle1/set_pen",SetPen)
          response = set_pen(r,g,b,width,off)
     except rospy.ServiceException as e:
          rospy.logwarn(e)

def pose_callback(pose:Pose):
    cmd=Twist()
    if pose.x>9.0 or pose.y>10 or pose.y<2:
            cmd.linear.x=1.0
            cmd.angular.z=3.0
        #cmd.angular.x=1.0
    elif pose.x<2.0 :#or y>8.0:
        cmd.linear.x=1.0
        cmd.angular.z=3.0
    else:
        cmd.linear.x=4.0
        cmd.angular.z=0.0
    #cmd.linear.x=10.0

    pub.publish(cmd)

if __name__=='__main__':
    rospy.init_node("controller")

    rospy.wait_for_service("turtle1/set_pen")

    call_set_pen_service(200,0,0,4,0)
    pub=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    
    sub=rospy.Subscriber("/turtle1/pose",Pose,callback=pose_callback)
    rospy.spin()

    