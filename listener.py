import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

def callback(msg):
    rospy.loginfo(msg)

def listener():
#topic name is /turtle1/cmd_vel, topic type is Twist
    rospy.init_node('listener',anonymous=True)
    rospy.Subscriber('chatter',String,callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
