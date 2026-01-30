import socket
import subprocess
import json

def take_photo():
    #print('take photo')
    filename='photo.jpg'
    subprocess.call(['python', 'modified_takephoto.py', '-savefile', str(filename)])


def server_program():
    # get the hostname
    host = socket.gethostname()
    print('HOST:', host)
    port = 6000
    server_socket = socket.socket()  # get instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    server_socket.bind(('', port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    while True:
	conn, address = server_socket.accept()  # accept new connection
	print("Connection from: " + str(address))
	#subprocess.call(['rostopic', 'pub' , '/spalladx_controller/command', 'std_msgs/Float64' , '1.6', '--once'])
	#take_photo()
	while True:
		# receive data stream. it won't accept data packet greater than 1024 bytes
		data = conn.recv(1024).decode()
		if not data:
		    # if data is not received break
		    break
		print("from connected user: " + data)

		#data = input(' -> ')
		filename = 'photo.jpg'
		take_photo()
		file = open(filename, 'rb')
		image_data = file.read()
		img_size = len(image_data)
		conn.send(str(img_size).encode())  # send data to the client
		conn.recv(1024) #wait for ack

		conn.sendall(image_data)
		conn.recv(1024) #wait for completition ack

	conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
