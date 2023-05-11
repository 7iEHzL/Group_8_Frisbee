import rospy
import numpy as np
import cv2

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count=0

    def callback(self, data):
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')

            # prepare rotate_cmd msg
            # DO NOT DELETE THE BELOW THREE LINES!
            msg = Header()
            msg = data.header
            msg.frame_id = '0'  # default: STOP

            # determine background color
            # TODO
            # determine the color and assing +1, 0, or, -1 for frame_id
            # msg.frame_id = '+1' # CCW (Blue background)
            # msg.frame_id = '0'  # STOP
            # msg.frame_id = '-1' # CW (Red background)
			
            self.count+=1
            image_flat = image[40:400,100:540]
            image_flatten = image_flat.reshape(image_flat.size//3,3)
            #print(image[240,320])
            
            colorCount = [0,0]
            
            red1 = image_flatten[image_flatten[:,0]<90,:]
            red2 = red1[red1[:,1]<90,:]
            redfinal = red2[red2[:,2]>200,:]
            colorCount[0] = redfinal.size//3
            
            blue1 = image_flatten[image_flatten[:,0]>200,:]
            blue2 = blue1[blue1[:,1]<150,:]
            bluefinal = blue2[blue2[:,2]<90,:]
            colorCount[1] = bluefinal.size//3
            
            print(colorCount[0]/(image_flatten.size//3))
            if colorCount[0] > (image_flatten.size//3) * 0.3:
                msg.frame_id = '-1'
            elif colorCount[1] > (image_flatten.size//3) * 0.3:
                msg.frame_id = '+1'
            else:
                msg.frame_id = '0'

            # publish color_state
            self.color_pub.publish(msg)
            
            #cv2.imshow('Image', image)
            #cv2.waitKey(1)

        except CvBridgeError as e:
            print(e)


    def rospy_shutdown(self, signal, frame):
        rospy.signal_shutdown("shut down")
        sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('CompressedImages1', anonymous=False)
    detector = DetermineColor()
    rospy.spin()
