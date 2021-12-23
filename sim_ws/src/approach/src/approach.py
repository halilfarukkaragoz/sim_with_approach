#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from math import pi
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from tf.msg import tfMessage
from math import sin, cos, pi


class approach:
    def __init__(self):
        rospy.init_node("approach")
        self.t = Twist()
        rospy.Subscriber("/odometry/filtered", Odometry, self.draw_spiral)
        rospy.Subscriber("/tf", tfMessage, self.detect_ar_tag)

        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        r = rospy.Rate(150)
        self.x_initial_point = 0
        self.y_initial_point = 0
        self.start_time = rospy.Time.now().secs
        self.linear_x = 0.4
        self.angular_z =pi / 3
        self.initilized = False
        self.sphiral_state = True
        self.look_around_state = False
        self.wait_for_ar_tag = False
        self.rotating = 0
        self.step = 0
        self.see_marker = 0
        self.r = 0
        self.return_speed_x = None
        self.return_speed_z = None

        r.sleep()
        rospy.spin()

    def draw_spiral(self, data):
        if (self.initilized == False):
            self.x_initial_point = data.pose.pose.position.x
            self.y_initial_point = data.pose.pose.position.y
            self.initilized = True

        self.x = data.pose.pose.position.x
        self.y = data.pose.pose.position.y
        self.z = data.pose.pose.position.z

        x_angular = data.pose.pose.orientation.x
        y_angular = data.pose.pose.orientation.y
        z_angular = data.pose.pose.orientation.z
        w_angular = data.pose.pose.orientation.w

        self.roll, self.pitch, self.yaw = euler_from_quaternion(
            (x_angular, y_angular, z_angular, w_angular))
        if(self.sphiral_state):
            self.speed()
        if(self.look_around_state):
            self.look_around()
        self.t.linear.x = self.linear_x
        self.t.angular.z = self.angular_z
        self.pub.publish(self.t)

    def find_distance(self,first,last):
        return np.sqrt(np.sum(np.square(np.subtract(first,last))))

    def speed(self):
        cur = rospy.Time.now().secs
        if (self.angular_z > 0):
            self.r = self.linear_x / self.angular_z
        print(self.r)
        if(int(cur-self.start_time) % 1.5 == 0 and self.r < 25):
            self.angular_z = 249 * self.angular_z/250
            self.linear_x = 121 * self.linear_x/120
            if(self.linear_x > 0.9 ):
                self.linear_x = 0.9
            self.step += 1
        if(self.find_distance([self.x_initial_point,self.y_initial_point],[self.x,self.y]) > 8):
            self.sphiral_state = False
            self.look_around_state = True
            self.starting_look_around = (rospy.Time.now().secs)
            self.rotating = self.yaw
            self.return_speed_x = self.linear_x
            self.return_speed_z = self.angular_z

    def detect_ar_tag(self, data):
        transform = data.transforms
        for i in transform:
            name = i.child_frame_id
            if "ar_marker_" in name:
                self.see_marker += 1
                self.return_speed_x = self.linear_x
                self.return_speed_z = self.angular_z
                self.linear_x = 0
                self.wait_for_ar_tag = True
                self.start_time = (rospy.Time.now().secs)
                self.angular_z = 0
                print("I see Ar_marker")
            if(((rospy.Time.now().secs) - self.start_time > 2 )and (self.see_marker < 5) and self.wait_for_ar_tag):
                self.wait_for_ar_tag = False
                self.sphiral_state = False
                self.look_around_state = True
                self.starting_look_around = (rospy.Time.now().secs)



    def look_around(self):
        self.linear_x = 0
        self.angular_z = pi
        if((rospy.Time.now().secs != self.starting_look_around) and abs(self.yaw - self.rotating) < 0.1):
            self.sphiral_state = True
            self.look_around_state = False
            self.linear_x = self.return_speed_x 
            self.angular_z = self.return_speed_z
            self.x_initial_point = self.x
            self.y_initial_point = self.y
            


if __name__ == "__main__":
    approach()
