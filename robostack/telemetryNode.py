#!/usr/bin/env python3
import rospy
from mavros_msgs.msg import State
from sensor_msgs.msg import NavSatFix

def stateCB(msg):
    # Logs connection status and current mode
    rospy.loginfo(f"Vehicle Connected: {msg.connected} | Mode: {msg.mode}")

def gpsCB(msg):
    # Logs GPS data
    rospy.loginfo(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")

if __name__ == '__main__':
    # Initialize ROS node
    rospy.init_node('navio2_telemetry_processor')
    
    # These subscribers process the raw MAVLink data translated by MAVROS
    rospy.Subscriber("mavros/state", State, stateCB)
    rospy.Subscriber("mavros/global_position/global", NavSatFix, gpsCB)
    
    rospy.spin()