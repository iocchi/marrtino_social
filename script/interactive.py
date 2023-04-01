#! /usr/bin/python

import sys,os
import time
sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

from robot_cmd_ros import *


#IN_TOPIC = "/social/face_nroface"
#IN_MSG   = Int32


tracking = False


def reset_face():    
    rospy.loginfo("Time is up, resetting face")
    #tilt_pub.publish(Float64(0))
    #pan_pub.publish(Float64(0))

def speech(msg):
    #rospy.loginfo('Speech : %s' %(msg))
    say(msg,'it')

def callback(data):
    global tracking
    if data.data == 0 and tracking:
        tracking = False
        #rospy.loginfo("No faces detected, resetting face in {} seconds".format(TIME_DELAY))
        #start_timer()

    elif data.data != 0 and not tracking:
        tracking = True
        #rospy.loginfo("Detected faces, stopping timer if started")
        speech("ciao")
        #stop_timer()

def wait_user_speaking(nsec):
    t_end = time.time()+nsec
    myasr = ''
    while time.time() < t_end:
        if myasr == '' :
            myasr = asr()    
        else :
            break
        return myasr
    

def listener():
    begin()
    #rospy.init_node("interactive")
    print("Interactive Mode Start")
    #rospy.Subscriber(IN_TOPIC,IN_MSG,callback)
    reset_face()
    speech("martina e pronta")
    speech("se vuoi puoi parlare con me ")
    speech("Collega il tablet o il telefono con l'applicazione ")
    speech("Attendo che tu lo faccia")
    mytxt = wait_user_speaking(5)
    print(mytxt)
    end()
     
listener()