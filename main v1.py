import rospy
import numpy as np
import cv2

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Header

#Filter = []
#gotFilt = False

class DetermineColor:
    '''def getFilter(self,imageflatten):
        global Filter, gotFilt
        try:
        	white1 = imageflatten[:,0]>120
        	white2 = imageflatten[:,1]>120
        	white3 = imageflatten[:,2]>120
        	Filter = np.logical_and(white1,white2,white3)
        	if Filter.size == imageflatten.size//3:
        	    gotFilt = True
        	else:
        	    raise Exception("SizeError")
        except Exception as error:
            print(type(error))
            print(error)
            return'''
	
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
            #image_flat = image[96:384,160:480]
            image_flatten = image.reshape(image.size//3,3)
            
            '''if not gotFilt:
                self.getFilter(image_flatten)
                return'''
            
            #print(image[240,320])
            
            colorCount = [0,0]
            
            #imageFiltered = image_flatten[Filter,:]
            imageFiltered = image_flatten
            
            red1 = imageFiltered[imageFiltered[:,0]<120,:]
            red2 = red1[red1[:,1]<110,:]
            redfinal = red2[red2[:,2]>190,:]
            colorCount[0] = redfinal.size//3
            
            blue1 = imageFiltered[imageFiltered[:,0]>190,:]
            blue2 = blue1[blue1[:,1]<160,:]
            bluefinal = blue2[blue2[:,2]<120,:]
            colorCount[1] = bluefinal.size//3
            
            print(colorCount[1]/(image_flatten.size//3))
            if colorCount[0] > (image_flatten.size//3) * 0.18:
                msg.frame_id = '-1'
            elif colorCount[1] > (image_flatten.size//3) * 0.15:
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
