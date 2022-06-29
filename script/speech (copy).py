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


SPEECH_TOPIC = "/speech/to_speak"
SPEECH_MSG   = String
  
def speech(testo):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,port))
    sock.send('TTS[it-IT]' + testo + '\n\r')
    data = sock.recv(80)
    sock.close


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I speech %s", data.data)
    speech(data.data)


def listener():
    rospy.init_node("speech_node")
    rospy.loginfo("speech node start")
    speech('speech node start')
    rospy.Subscriber(SPEECH_TOPIC,SPEECH_MSG,callback)
    rospy.spin()

listener()
