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

    tmux = TmuxSend('bringup', ['netcat','social','speech','cmd'])

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
                print("rec [%s]" %data)
                rfolder = "~/src/marrtino_social/launch"
                cfolder = "~/src/marrtino_social/config"
                sfolder = "~/src/marrtino_social/script"
                homefolder = "~/src/marrtino_social"


                # social functions (emotions)
                if data=='@social':
                    tmux.cmd(1,'cd %s' %rfolder)
                    tmux.cmd(1,'roslaunch rosbridge.launch')   
                elif data=='@socialkill':
                    tmux.Cc(1)
             
                # social normale con pan e tilt
                if data=='@robotsocial':
                    tmux.cmd(1,'cd %s' %rfolder)
                    tmux.cmd(1,'roslaunch social.launch')   
                elif data=='@robotsocialkill':
                    tmux.Cc(1)

                # start social no servo demo
                elif data=='@socialnoservo': 
                    tmux.cmd(1,'cd %s' %rfolder)
                    tmux.cmd(1,'roslaunch socialnoservo.launch')
                elif data=='@socialnoservokill':
                    tmux.Cc(1)

                # social no tracker face
                elif data=='@socialnotracker': 
                    tmux.cmd(1,'cd %s' %rfolder)
                    tmux.cmd(1,'roslaunch socialnotracker.launch')
                elif data=='@socialnotrackerkill': 
                    tmux.Cc(1)

                

                elif (data=='@updatesocialapps'):
                    print('marrtino_apps update')
                    #self.setStatus('Updating...')
                    tmux.cmd(3,'cd %s' %homefolder)
                    tmux.cmd(3,'git pull', blocking=True)
                    time.sleep(1)
                    #self.checkStatus()


               
                # start speech_start ( 2 speech)
                elif data=='@speech': 
                    tmux.cmd(2,'cd %s' %sfolder)
                    tmux.cmd(2,'python interactive.py')
                elif data=='@speechkill':
                    tmux.Cc(2)
                                
                else:
                    print('Unknown command %s' %data)



if __name__ == '__main__':

    default_port = 9250

    parser = argparse.ArgumentParser(description='social bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

