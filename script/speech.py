#! /usr/bin/python
import rospy
import sys
import socket
import time
from std_msgs.msg import String

print("*******************************")
print("**********  speech.py *********")
print("*******************************")

ip = '127.0.0.1'
port = 9001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip,port))
SPEECH_TOPIC = "/speech/to_speak"
SPEECH_MSG   = String
  

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I speech %s", data.data)
    sock.send('TTS[it-IT]' + data.data + '\n\r')
    data = sock.recv(80)
    #print data


def listener():
    rospy.init_node("speech_node")
    rospy.loginfo("speech node start")
    sock.send('TTS[it-IT] speech node start\n\r')
    rospy.Subscriber(SPEECH_TOPIC,SPEECH_MSG,callback)
    rospy.spin()

listener()
