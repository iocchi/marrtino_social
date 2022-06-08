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

    tmux = TmuxSend('bringup', ['netcat','social','tracker','speech','cmd'])

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
             
                # social normale con pan e tilt
                if data=='@robotsocial':
                    tmux.cmd(1,'cd %s' %rfolder)
                    tmux.cmd(1,'roslaunch social.launch')   
                elif data=='@robotsocialkill':
                    tmux.Cc(1)

                # start social no servo 
                elif data=='@social': 
                    tmux.cmd(1,'cd %s' %rfolder)
                    tmux.cmd(1,'roslaunch socialnoservo.launch')
                elif data=='@socialkill':
                    tmux.Cc(1)

                # tracker
                elif data=='@tracker': 
                    tmux.cmd(2,'cd %s' %rfolder)
                    tmux.cmd(2,'roslaunch tracker.launch')
                elif data=='@trackerkill': 
                    tmux.Cc(2)
                                
                else:
                    print('Unknown command %s' %data)



if __name__ == '__main__':

    default_port = 9250

    parser = argparse.ArgumentParser(description='social bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

