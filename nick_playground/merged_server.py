#!/usr/bin/env python2
from __future__ import print_function  # allow print(...) in Py2

import socket
import threading
import subprocess
import json
import os
import rospy
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist
import queue

# ---------------------------
# Useful logging function
# ---------------------------
log_queue = queue.Queue()

def log(message):
    """Enqueue a log message."""
    log_queue.put(message)

def flush_logs():
    """Flush log messages from the queue by printing them in the main thread."""
    while not log_queue.empty():
        msg = log_queue.get()
        print(msg)

# ---------------------------
# Marrtina VISION functions
# ---------------------------

def take_photo(filename):
    """
    Calls a script (my_mod_takephoto.py) that takes a photo and saves it as filename.
    Returns YOLO detection results (read from "yolo_result.txt").
    """
    try:
        # Launch the photo-taking process under the system's default 'python'
        subprocess.call(['python', 'modified_takephoto.py', '-savefile', str(filename)])
        result_file = "yolo_result.txt"
        if os.path.exists(result_file):
            with open(result_file, "r") as f:
                yolo_result = f.read().strip()
        else:
            yolo_result = "No result"
        log("[INFO] YOLO Result: %s" % yolo_result)
        return yolo_result
    except Exception as e:
        log("[ERROR] Failed to take photo: %s" % e)
        return "Error taking photo"

def handle_get_img(conn):
    """
    Handles the 'get_img' command.
    Takes a photo, reads the image, and sends the image size, image data, and YOLO result back.
    """
    try:
        log("[INFO] Processing image request...")
        filename = 'photo.jpg'
        # Take a photo (and run YOLO processing)
        yolo_result = take_photo(filename)

        # Read the image data
        with open(filename, 'rb') as file_:
            image_data = file_.read()
        
        # Send the Yolo result 
        conn.sendall((yolo_result + '\n').encode())

        # Send image size to the client
        img_size = len(image_data)
        conn.sendall((str(img_size) + '\n').encode())  

        # Send the image data
        conn.sendall(image_data)

    except Exception as e:
        log("[ERROR] in handle_get_img: %s" % e)
        conn.sendall("Error in get_img")

# ---------------------------
# Marrtina MOVEMENT functions
# ---------------------------

movement_publishers = {}

def init_movement_publishers():
    """
    Initializes all ROS publishers for movement commands only once.
    """
    global movement_publishers
    movement_publishers['cmd_vel'] = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    movement_publishers['pan_controller'] = rospy.Publisher('pan_controller/command', Float64, queue_size=1, latch=True)
    movement_publishers['tilt_controller'] = rospy.Publisher('tilt_controller/command', Float64, queue_size=1, latch=True)
    movement_publishers['shoulderdx_rotate'] = rospy.Publisher('shoulderdx_rotate/command', Float64, queue_size=1, latch=True)
    movement_publishers['shouldersx_rotate'] = rospy.Publisher('shouldersx_rotate/command', Float64, queue_size=1, latch=True)
    movement_publishers['shoulderdx_open'] = rospy.Publisher('shoulderdx_open/command', Float64, queue_size=1, latch=True)
    movement_publishers['shouldersx_open'] = rospy.Publisher('shouldersx_open/command', Float64, queue_size=1, latch=True)
    movement_publishers['elbowdx_rotate'] = rospy.Publisher('elbowdx_rotate/command', Float64, queue_size=1, latch=True)
    movement_publishers['elbowsx_rotate'] = rospy.Publisher('elbowsx_rotate/command', Float64, queue_size=1, latch=True)
    movement_publishers['elbowdx_open'] = rospy.Publisher('elbowdx_open/command', Float64, queue_size=1, latch=True)
    movement_publishers['elbowsx_open'] = rospy.Publisher('elbowsx_open/command', Float64, queue_size=1, latch=True)
    log("[INFO] Movement publishers initialized.")

def handle_move_robot(conn, data):
    """
    Handles movement commands.
    Expects data as a JSON string with movement instructions.
    Publishes commands to appropriate ROS topics.
    """
    try:
        # Parse the JSON data
        if data.startswith("move_robot "):
            data = data[len("move_robot "):]

        cmd_data = json.loads(data)
        log("[INFO] Received movement command: %s" % cmd_data)

        # Extract all values as floats
        pan_controller = float(cmd_data.get('pan_controller'))
        tilt_controller = float(cmd_data.get('tilt_controller'))
        shoulder_dx_rotate = float(cmd_data.get('shoulder_dx_rotate'))
        shoulder_sx_rotate = float(cmd_data.get('shoulder_sx_rotate'))
        shoulder_dx_open = float(cmd_data.get('shoulder_dx_open'))
        shoulder_sx_open = float(cmd_data.get('shoulder_sx_open'))
        elbow_dx_rotate = float(cmd_data.get('elbow_dx_rotate'))
        elbow_sx_rotate = float(cmd_data.get('elbow_sx_rotate'))
        elbow_dx_open = float(cmd_data.get('elbow_dx_open'))
        elbow_sx_open = float(cmd_data.get('elbow_sx_open'))
        
        # For demonstration, we assume the JSON includes a cmd_vel field
        if 'cmd_vel' in cmd_data:
            cmd_vel_msg = Twist()
            cmd_vel_msg.linear.x = float(cmd_data["cmd_vel"]["linear"]["x"])
            cmd_vel_msg.linear.y = float(cmd_data["cmd_vel"]["linear"]["y"])
            cmd_vel_msg.linear.z = float(cmd_data["cmd_vel"]["linear"]["z"])
            cmd_vel_msg.angular.x = float(cmd_data["cmd_vel"]["angular"]["x"])
            cmd_vel_msg.angular.y = float(cmd_data["cmd_vel"]["angular"]["y"])
            cmd_vel_msg.angular.z = float(cmd_data["cmd_vel"]["angular"]["z"])
            movement_publishers['cmd_vel'].publish(cmd_vel_msg)

        else:
            if pan_controller is not None:
                movement_publishers['pan_controller'].publish(Float64(float(cmd_data['pan_controller'])))
                
            if tilt_controller is not None:
                movement_publishers['tilt_controller'].publish(Float64(float(cmd_data['tilt_controller'])))
                
            if shoulder_dx_rotate is not None:
                movement_publishers['shoulderdx_rotate'].publish(Float64(float(cmd_data['shoulder_dx_rotate'])))
                
            if shoulder_sx_rotate is not None:
                movement_publishers['shouldersx_rotate'].publish(Float64(float(cmd_data['shoulder_sx_rotate'])))
                
            if shoulder_dx_open is not None:
                movement_publishers['shoulderdx_open'].publish(Float64(float(cmd_data['shoulder_dx_open'])))
                
            if shoulder_sx_open is not None:
                movement_publishers['shouldersx_open'].publish(Float64(float(cmd_data['shoulder_sx_open'])))
                
            if elbow_dx_rotate is not None:
                movement_publishers['elbowdx_rotate'].publish(Float64(float(cmd_data['elbow_dx_rotate'])))
               
            if elbow_sx_rotate is not None:
                movement_publishers['elbowsx_rotate'].publish(Float64(float(cmd_data['elbow_sx_rotate'])))
                
            if elbow_dx_open is not None:
                movement_publishers['elbowdx_open'].publish(Float64(float(cmd_data['elbow_dx_open'])))
                
            if elbow_sx_open is not None:
                movement_publishers['elbowsx_open'].publish(Float64(float(cmd_data['elbow_sx_open'])))
                

    except Exception as e:
        log("[ERROR] in handle_move_robot: %s" % e)
        conn.sendall("Error in move_robot")

# ---------------------------
# Marrtina FACE functions
# ---------------------------

def handle_set_face(conn, data):
    """
    Handles the 'set_face' command.
    Expects data as a JSON string with an 'emotion' key.
    Publishes the emotion to the ROS topic /social/emotion.
    """
    try:
        parsed = json.loads(data)
        emotion = parsed.get('emotion')
        if emotion:
            pub = rospy.Publisher('/social/emotion', String, queue_size=10)
            pub.publish(emotion)
            log("[INFO] Published emotion: %s" % emotion)
        else:
            log("[WARNING] Invalid input given")
            conn.sendall("Invalid emotion command")
    except Exception as e:
        log("[ERROR] in handle_set_face: %s" % e)
        conn.sendall("Error in set_face")

# ---------------------------
# Client Handler
# ---------------------------

def client_handler(client_conn):
    while True:
        try:
            data = client_conn.recv(4096).strip()
            if not data:
                break
            log("[INFO] Received command: %s" % data)

            if data.startswith("get_img"):
                threading.Thread(target=handle_get_img, args=(client_conn,)).start()
            elif data.startswith("move_robot"):
                threading.Thread(target=handle_move_robot, args=(client_conn, data)).start()
            elif data.startswith("set_face"):
                threading.Thread(target=handle_set_face, args=(client_conn, data)).start()
            else:
                client_conn.sendall("Unknown command")
        except Exception as e:
            log("[ERROR] in client_handler: %s" % e)
            break

    log("[INFO] Closing client connection.")
    client_conn.close()

# ---------------------------
# Main Server Function
# ---------------------------

def main():
    rospy.init_node('unified_server_node', anonymous=True)
    init_movement_publishers()

    server_port = 9000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', server_port))
    s.listen(5)
    log("[INFO] Server listening on port %d" % server_port)

    try:
        while True:
            client_conn, addr = s.accept()
            print("[INFO] New client connected from %s:%d" % (addr[0], addr[1]))
            client_handler(client_conn)
            flush_logs()
    except KeyboardInterrupt:
        print("[INFO] Shutting down server (CTRL+C received)")
    finally:
        s.close()

if __name__ == '__main__':
    main()
