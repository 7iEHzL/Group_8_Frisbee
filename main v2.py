import rospy
import numpy as np
import cv2

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

massFilt = np.zeros(480*640)
image_flatten = np.zeros((480*640,3))
lastimage = None

class DetermineColor:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/camera/color/image_raw', Image, self.callback)
        self.color_pub = rospy.Publisher('/rotate_cmd', Header, queue_size=10)
        self.bridge = CvBridge()
        self.count=0
        
    def deltaImage(self,img,lastimg):
        global massFilt
        delta = img - lastimg
        held = np.logical_or(
        		np.logical_and( delta[:,0] > 40 , delta[:,0] < 215 ),
        		np.logical_and( delta[:,1] > 40 , delta[:,1] < 215 ),
        		np.logical_and( delta[:,2] > 40 , delta[:,2] < 215 )
        	)
        '''if np.sum(held)>100:
            print(127.5-abs(delta[240*320]-127.5))'''
        massFilt = massFilt + held
        return

    def callback(self, data):
        global image_flatten, massFilt, lastimage
        try:
            # listen image topic
            image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
            
            image_flatten = image.reshape(image.size//3,3)
            if self.count % 100 == 0:
                if lastimage is None:
                    lastimage = np.zeros((480*640,3))
                self.deltaImage(image_flatten,lastimage)
                lastimage = image_flatten

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
            
            colorCount = [0.00,0.00]
            
            red1 = image_flatten[:,0]<90
            red2 = image_flatten[:,1]<140
            red3 = image_flatten[:,2]>180
            redfinal = np.logical_and(red1,red2,red3) * massFilt / np.sum(massFilt)
            colorCount[0] = np.sum(redfinal)
            
            blue1 = image_flatten[:,0]>170
            blue2 = image_flatten[:,1]<200
            blue3 = image_flatten[:,2]<100
            bluefinal = np.logical_and(blue1,blue2,blue3) * massFilt / np.sum(massFilt)
            colorCount[1] = np.sum(bluefinal)
            
            #print("[%3d,%3d,%3d]" % (image[240,320,2],image[240,320,1],image[240,320,0]))
            print("%.3f %.3f" % (colorCount[0], colorCount[1]))
            
            if colorCount[0] >= 0.40:
                msg.frame_id = '-1'
            elif colorCount[1] >= 0.40:
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
