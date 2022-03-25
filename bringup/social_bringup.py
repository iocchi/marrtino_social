#!/usr/bin/env python

from __future__ import print_function

import thread
import socket

import argparse

import sys, time, os, glob, shutil, math, datetime

from tmuxsend import TmuxSend


def run_server(port):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.settimeout(3)
    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)
    sock.listen(1)
    print("ROS social server started on port %d ..." %port)

    tmux = TmuxSend('social', ['robot','cmd'])

    connected = False
    dorun = True
    while dorun:

        if not connected:
            print("-- Waiting for connection ...")
        while (dorun and not connected):
            try:
                # Wait for a connection
                connection, client_address = sock.accept()
                connected = True
                print ('-- Connection from %s'  %client_address[0])
            except KeyboardInterrupt:
                print("User interrupt (quit)")
                dorun = False
            except Exception as e:
                print(e)
                pass # keep listening
    
        if not dorun:
            return

        # print("-- Waiting for data...")
        data = None
        while dorun and connected and data is None:
            # receive data
            try:
                #connection.settimeout(3) # timeout when listening (exit with CTRL+C)
                data = connection.recv(320)  # blocking
                data = data.strip()
            except KeyboardInterrupt:
                print("User interrupt (quit)")
                dorun = False
            except socket.timeout:
                data = None
                print("socket timeout")

        if data is not None:
            if len(data)==0:
                connected = False
            else:
                print(data)
                rfolder = "~/src/marrtino_social/launch"
                cfolder = "~/src/marrtino_social/config"
                if data=='@robot_social':
                    #tmux.cmd(0,"echo '@robot' | netcat -w 1 localhost 9236") # robot
                    tmux.cmd(0,"echo '@joystick' | netcat -w 1 localhost 9240") # teleop joy
                    
                   
                elif data=='@robot_socialkill':
                    tmux.Cc(0)

                elif data=='@tracker': 
                    tmux.cmd(0,'cd %s' %rfolder)
                    tmux.cmd(0,'roslaunch tracker.launch')
                
                elif data=='@trackerkill':
                    tmux.Cc(0)

                elif data=='@social':
                    #tmux.cmd(0,"echo '@usbcam' | netcat -w 1 localhost 9237") # webcam
                    tmux.cmd(0,'cd %s' %rfolder)
                    #tmux.cmd(0,'roslaunch social.launch')
                    tmux.cmd(0,"roslaunch talk talk.launch")
                    time.sleep(1)
                    tmux.cmd(0,"roslaunch speech speech.launch")
                    time.sleep(1)
                    tmux.cmd(0,'cd %s' %rfolder)
                    tmux.cmd(0,'roslaunch tracker.launch')
                    time.sleep(1)


                    tmux.cmd(0,'roslaunch social.launch')
                    time.sleep(5)
                    tmux.cmd(0,"rostopic pub -1 /tilt_controller/command std_msgs/Float64 0") 
                    tmux.cmd(0,"rostopic pub -1 /pan_controller/command std_msgs/Float64 0") 
                    #self.waitfor('social',5)
                    time.sleep(1)
                    #tmux.cmd(0,"DISPLAY=:0 midori -e Fullscreen -a  http://localhost/social/marrtina.html &")
                    #time.sleep(6)
                    tmux.cmd(0,"rostopic pub -1 /social/emotion std_msgs/String \"startblinking\"")
                    time.sleep(1)
                    tmux.cmd(0,"rostopic pub -1 /talk/to_talk std_msgs/String \"ciao sono martina e sono operativa\"")
   
                elif data=='@socialkill':
                    tmux.Cc(0)
                
                else:
                    print('Unknown command %s')



if __name__ == '__main__':

    default_port = 9250

    parser = argparse.ArgumentParser(description='social bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

