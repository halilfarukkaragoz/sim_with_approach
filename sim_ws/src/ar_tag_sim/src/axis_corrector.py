#!/usr/bin/env python 

# Halil Faruk Karagoz 
# At first i wrote this for fixing the axis then it was working correct than we fixed it with static frame 
#After this code wasn't necessary to use but still couldn't delete it bcs it was my first proper ros code <kiyamadim>
import rospy 
import tf2_geometry_msgs
import tf
from geometry_msgs.msg import Transform
from math import pi
from fiducial_msgs.msg import FiducialTransformArray,FiducialTransform


class axis_correction:
    def __init__(self):
        self.correct_transforms = FiducialTransformArray()
        rospy.init_node("axis_corrector")
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        rospy.Subscriber("/fiducial_transforms",FiducialTransformArray,self.fiducial_correct)
        self.pub = rospy.Publisher("/fiducial_correct",FiducialTransform,queue_size=10)
        rospy.spin()


    def fiducial_correct(self,data):
        self.correct_transforms.header = data.header
        self.correct_transforms.image_seq = data.image_seq
        for i in data.transforms:
            self.correct_transform = FiducialTransform()

            self.correct_transform.fiducial_id = i.fiducial_id
            self.correct_transform.image_error = i.image_error
            self.correct_transform.object_error = i.object_error
            self.correct_transform.fiducial_area = i.fiducial_area


            self.correct_transform.transform.translation.x = i.transform.translation.z
            self.correct_transform.transform.translation.y = -i.transform.translation.x
            self.correct_transform.transform.translation.z = -i.transform.translation.y
            
            self.roll,self.pitch,self.yaw = tf.transformations.euler_from_quaternion([i.transform.rotation.x,i.transform.rotation.y,i.transform.rotation.z,i.transform.rotation.w])
            x,y,z,w = tf.transformations.quaternion_from_euler(self.yaw,-self.roll + pi/2,-self.pitch)
            self.correct_transform.transform.rotation.x = x
            self.correct_transform.transform.rotation.y = y
            self.correct_transform.transform.rotation.z = z
            self.correct_transform.transform.rotation.w = w
            self.pub.publish(self.correct_transform)
            transform = (self.correct_transform.transform.translation.x,self.correct_transform.transform.translation.y,self.correct_transform.transform.translation.z)
            rotation = (self.correct_transform.transform.rotation.x,self.correct_transform.transform.rotation.y,self.correct_transform.transform.rotation.z,self.correct_transform.transform.rotation.w)

            self.br.sendTransform(transform,
                        rotation,
                        rospy.Time.now(),
                        str(self.correct_transform.fiducial_id),
                        "camera"
                        )
            #print(type(("ar_marker %d",data.id)))
if __name__ == "__main__":
    axis_correction()





    
