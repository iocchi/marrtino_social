import socket
import subprocess
import json
import time
import threading
import rospy
from subprocess import call
from std_msgs.msg import String,Float64
from geometry_msgs.msg import Twist


def take_photo(filename):
    call(['python', 'my_takephoto.py', '-savefile', str(filename)])

def server_program():
    global waiting_active
    host = socket.gethostname()
    print('HOST', host)
    port = 7000
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('',port))
    while True:
	    server_socket.listen(2)
	    conn, address = server_socket.accept()
	    print('Connection from: ', str(address))
	    rospy.init_node('Server_node', anonymous=True)

            tilt_publisher = rospy.Publisher('tilt_controller/command', Float64, queue_size=1, latch=True)
            pan_publisher = rospy.Publisher('pan_controller/command', Float64, queue_size=1, latch=True)

	    sdx_open_publisher = rospy.Publisher('shoulderdx_open/command', Float64, queue_size=1, latch=True)
	    ssx_open_publisher = rospy.Publisher('shouldersx_open/command', Float64, queue_size=1, latch=True)
	    sdx_rotate_publisher = rospy.Publisher('shoulderdx_rotate/command', Float64, queue_size=1, latch=True)
	    ssx_rotate_publisher = rospy.Publisher('shouldersx_rotate/command', Float64, queue_size=1, latch=True)

	    edx_open_publisher = rospy.Publisher('elbowdx_open/command', Float64, queue_size=1, latch=True)
	    esx_open_publisher = rospy.Publisher('elbowsx_open/command', Float64, queue_size=1, latch=True)
	    edx_rotate_publisher = rospy.Publisher('elbowdx_rotate/command', Float64, queue_size=1, latch=True)
	    esx_rotate_publisher = rospy.Publisher('elbowsx_rotate/command', Float64, queue_size=1, latch=True)

            cmd_vel_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)


	    while True:
		try:
		        data = conn.recv(1024).decode()
		        if not data:
		            break
		        print('from connected user: ', data)
		        data = json.loads(json.loads(data))

			takephoto = data.get('takephoto')
		        pan_controller = float(data.get('pan_controller'))
			tilt_controller = float(data.get('tilt_controller'))
			emotion = data.get('emotion')
			shoulder_dx_rotate = float(data.get('shoulder_dx_rotate'))
			shoulder_sx_rotate = float(data.get('shoulder_sx_rotate'))
			shoulder_dx_open = float(data.get('shoulder_dx_open'))
			shoulder_sx_open = float(data.get('shoulder_sx_open'))
			elbow_dx_rotate = float(data.get('elbow_dx_rotate'))
			elbow_sx_rotate = float(data.get('elbow_sx_rotate'))
			elbow_dx_open = float(data.get('elbow_dx_open'))
			elbow_sx_open = float(data.get('elbow_sx_open'))
                        if 'cmd_vel' in data:
                        	cmd_vel_msg = Twist()
                        	cmd_vel_msg.linear.x = float(data["cmd_vel"]["linear"]["x"])
                        	cmd_vel_msg.linear.y = float(data["cmd_vel"]["linear"]["y"])
                        	cmd_vel_msg.linear.z = float(data["cmd_vel"]["linear"]["z"])
                        	cmd_vel_msg.angular.x = float(data["cmd_vel"]["angular"]["x"])
                        	cmd_vel_msg.angular.y = float(data["cmd_vel"]["angular"]["y"])
                        	cmd_vel_msg.angular.z = float(data["cmd_vel"]["angular"]["z"])
				cmd_vel_publisher.publish(cmd_vel_msg)

			if takephoto == 'True':
				print('Taking photo')
				filename = 'photo.jpg'
				take_photo(filename)
				#time.sleep(1)
				file = open(filename,'rb')
				image_data = file.read()
				img_size = len (image_data)
				conn.send(str(img_size).encode()) #send image length to client
				conn.recv(1024) #wait for ack

				conn.sendall(image_data)
				conn.recv(1024) #wait for completition ack
				#count = 0
				#while image_data:
					#print('Chunk: ', count)
					#count = count+1
					#conn.send(image_data)
					#image_data = file.read(2048)
				#file.close()

			else:
				if pan_controller != None:
					pan_publisher.publish(Float64(pan_controller))
				if tilt_controller != None:
					tilt_publisher.publish(Float64(tilt_controller))
				if emotion != None:
					pass
				if shoulder_dx_rotate != None:
					sdx_rotate_publisher.publish(Float64(shoulder_dx_rotate))
				if shoulder_sx_rotate != None:
					ssx_rotate_publisher.publish(Float64(shoulder_sx_rotate))

				if shoulder_dx_open != None:
					sdx_open_publisher.publish(Float64(shoulder_dx_open))
				if shoulder_sx_open != None:
					ssx_open_publisher.publish(Float64(shoulder_sx_open))


				if elbow_dx_rotate != None:
					edx_rotate_publisher.publish(Float64(elbow_dx_rotate))
				if elbow_sx_rotate != None:
					esx_rotate_publisher.publish(Float64(elbow_sx_rotate))
				if elbow_dx_open != None:
					edx_open_publisher.publish(Float64(elbow_dx_open))
				if elbow_sx_open != None:
					esx_open_publisher.publish(Float64(elbow_sx_open))
                                #if cmd_vel != None:
                                        #cmd_vel_publisher.publish(cmd_vel_msg)

			#print('SENDING ACK')
			#conn.send('ackkkk'.encode())
		except:
			print('Invalid input')
	    conn.close()

            time.sleep(2)

if __name__ == '__main__':
    server_program()
