#!/usr/bin/env python

#Halil Faruk Karagoz

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError 
import os

class take_photo:
    def __init__(self):
        rospy.init_node("take_photo");
        self.bridge = CvBridge(); 
        self.cv_image = None
        rospy.Subscriber("/camera/image_raw",Image,self.camera_img);

        self.flag_over_exposured = False
        self.flag_low_exposured = False

        self.exposure = 100
        self.gain = 30
        self.upper_limit_gain = False
        self.lower_limit_gain = False
    
        self.upper_limit_exposure = False
        self.lower_limit_exposure = False
        self.dir_names = []
        self.use_filter = False
        self.count = 0
        self.starting_time = rospy.Time.now().secs

        self.rate = rospy.Rate(10)
        self.take_input()
    def camera_img(self,data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
               


    def take_input(self):
        while not rospy.is_shutdown():
            self.class_name = raw_input("write_your_class_name: ")
            if not(self.class_name in self.dir_names):
                os.mkdir("/",self.class_name)
                self.dir_names.append(self.class_name)
            
            cv2.imwrite(str(self.class_name) + "/" + str(self.count) +  ".png",self.cv_image)
            self.count +=1
            self.rate.sleep()



if __name__ == "__main__":
    take_photo();
