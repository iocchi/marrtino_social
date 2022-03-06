# from social port 9991

from __future__ import print_function

import socket
import time
import os

from threading import Thread

import sys

# http://www.html.it/pag/53419/websocket-server-con-python/
# sudo -H pip install tornado

try:
    import tornado.httpserver
    import tornado.websocket
    import tornado.ioloop
    import tornado.web
except Exception as e:
    print(e)
    print('Install tornado: pip install --user tornado')
    sys.exit(0)

#sys.path.append('../program')
sys.path.append('scripts')

import check
from check import *

from tmuxsend import TmuxSend

# Global variables

websocket_server = None     # websocket handler
run = True                  # main_loop run flag
server_name = 'Bringup'     # server name
server_port = 9991          # web server port social
status = "Idle"             # robot status sent to websocket


# Websocket server handler

class MyWebSocketServer(tornado.websocket.WebSocketHandler):

    def checkStatus(self, what='ALL'):

        self.setStatus('Checking...')
        r = check_ROS()
        self.write_message('RESULT ros '+str(r))
        if (r):
            rospy.init_node('marrtino_bringup', disable_signals=True)
            self.write_message('VALUE rosnodes %r' %check.nodenames)
            self.write_message('VALUE rostopics %r' %check.topicnames)

        if (what=='robot' or what=='ALL'):
            r = check_robot()
            self.write_message('RESULT robot '+str(r))
            r = check_odom()
            self.write_message('RESULT odom '+str(r))
            r = check_social()
            self.write_message('RESULT social '+str(r))

        

        self.setStatus('Idle')
        time.sleep(1)
        self.setStatus('Idle')


    def setStatus(self, st):
        global status
        status = st
        self.write_message('STATUS %s' %status)


    def open(self):
        global websocket_server, run
        websocket_server = self
        print('>>> New connection <<<')
        self.setStatus('Executing...')
        self.winlist = ['cmd','roscore','quit','wsrobot','modim',
                        'robot','waypoint','rviz','imgproc','joystick','audio',
                        'map_loc','navigation','playground','netcat','navi','social']

        self.wroscore = self.winlist.index('roscore')
        self.wrobot = self.winlist.index('robot')
        self.wwaypoint = self.winlist.index('waypoint')
        self.wrviz = self.winlist.index('rviz')
        self.wimgproc = self.winlist.index('imgproc')
        self.wjoystick = self.winlist.index('joystick')
        self.waudio = self.winlist.index('audio')
        self.wwsrobot = self.winlist.index('wsrobot')
        self.wquit = self.winlist.index('quit')
        self.wmodim = self.winlist.index('modim')
        self.wmaploc = self.winlist.index('map_loc')
        self.wnav = self.winlist.index('navigation')
        self.wplayground = self.winlist.index('playground')
        self.wnet = self.winlist.index('netcat')
        self.wnavi = self.winlist.index('navi')
        self.wsocial = self.winlist.index('social')
        self.tmux = TmuxSend('bringup',self.winlist)
        self.tmux.roscore(self.wroscore)
        time.sleep(1)
        #self.tmux.cmd(self.wmodim,'cd $MODIM_HOME/src/GUI')
        #self.tmux.cmd(self.wmodim,'python ws_server.py -robot marrtino')
        time.sleep(1)
        #self.wsrobot()
        #time.sleep(3)

        self.checkStatus()

        print("----")
        sys.stdout.flush()
       

    def waitfor(self, what, timeout):
        time.sleep(2)
        r = check_it(what)
        while not r and timeout>0:
            time.sleep(1)
            timeout -= 1
            r = check_it(what)
        self.write_message('RESULT %s %s' %(what,str(r)))



    def on_message(self, message):    
        print('>>> MESSAGE RECEIVED: %s <<<' %message)
        self.setStatus(message)

        try:
            self.process_message(message)
        except:
            print("Error in message %s" %message)

        print("----")
        sys.stdout.flush()

        self.setStatus('Idle')

    def process_message(self, message):
        global code, status

        print('Code --> received:\n%s' %message)
 
        if (message=='stop'):
            print('!!! EMERGENCY STOP !!!')
            self.checkStatus()

        elif (message=='check'):
            self.checkStatus()

        elif (message=='ros_quit'):
            self.tmux.quitall(range(5,len(self.winlist)))
            self.checkStatus()

        # robot start/stop
        elif (message=='robot_start'):
            self.tmux.cmd(self.wnet,"echo '@robot' | netcat -w 1 localhost 9236")
            self.tmux.roslaunch(self.wrobot,'launch','robot')
            self.waitfor('robot',5)
            self.waitfor('odom',1)
            #self.waitfor('sonar',1)
        elif (message=='robot_kill'):
            self.tmux.cmd(self.wnet,"echo '@robotkill' | netcat -w 1 localhost 9236")
            self.tmux.roskill('orazio')
            self.tmux.roskill('state_pub_robot')
            time.sleep(1)
            self.tmux.killall(self.wrobot)
            time.sleep(1)
            if check_robot():
                self.tmux.cmd(wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
                time.sleep(1)
            while check_robot():
                time.sleep(1)
            self.write_message('RESULT robot False')
            #self.checkStatus('robot')

        #  social start/stop
        elif (message=='social_start'):
            self.tmux.cmd(self.wnet,"echo '@social' | netcat -w 1 localhost 9236")
            self.tmux.roslaunch(self.wsocial,'launch','social')
            self.waitfor('social',5)
            time.sleep(1)
            self.tmux.cmd(self.wnet,"rostopic pub -1 /tilt_controller/command std_msgs/Float64 0") 
            self.tmux.cmd(self.wnet,"rostopic pub -1 /pan_controller/command std_msgs/Float64 0") 
           
            time.sleep(1)
            self.tmux.cmd(self.wnet,"DISPLAY=:0 midori -e Fullscreen -a  http://localhost/social/marrtina.html &")
            time.sleep(6)
            self.tmux.cmd(self.wnet,"rostopic pub -1 /social/emotion std_msgs/String \"startblinking\"")
            time.sleep(1)
            self.tmux.cmd(self.wnet,"rostopic pub -1 /talk/to_talk std_msgs/String \"ciao sono martina e sono operativa\"")
           
        elif (message=='social_kill'):
            self.tmux.cmd(self.wnet,"echo '@socialkill' | netcat -w 1 localhost 9236")
            #self.tmux.roskill('orazio')
            #self.tmux.roskill('state_pub_robot')
            time.sleep(1)
            self.tmux.killall(self.wsocial)
            time.sleep(1)
            if check_robot():
                self.tmux.cmd(wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
                time.sleep(1)
            while check_robot():
                time.sleep(1)
            self.write_message('RESULT robot False')
            #self.checkStatus('robot')

         # social headstart/stop
        elif (message=='socialhead_start'):
            self.tmux.cmd(self.wnet,"echo '@social' | netcat -w 1 localhost 9236")
            self.tmux.roslaunch(self.wsocial,'launch','socialhead')
            self.waitfor('social',5)
            #self.waitfor('odom',1)
            #self.waitfor('sonar',1)
        elif (message=='socialhead_kill'):
            self.tmux.cmd(self.wnet,"echo '@socialkill' | netcat -w 1 localhost 9236")
            #self.tmux.roskill('orazio')
            #self.tmux.roskill('state_pub_robot')
            time.sleep(1)
            self.tmux.killall(self.wsocial)
            time.sleep(1)
            if check_robot():
                self.tmux.cmd(wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
                time.sleep(1)
            while check_robot():
                time.sleep(1)
            self.write_message('RESULT robot False')
            #self.checkStatus('robot')
        
        # robot start/stop
        elif (message=='socialnf_start'):
            self.tmux.cmd(self.wnet,"echo '@social' | netcat -w 1 localhost 9236")
            self.tmux.roslaunch(self.wsocial,'launch','socialnoface')
            self.waitfor('social',5)
            #self.waitfor('odom',1)
            #self.waitfor('sonar',1)
        elif (message=='socialnf_kill'):
            self.tmux.cmd(self.wnet,"echo '@socialkill' | netcat -w 1 localhost 9236")
            #self.tmux.roskill('orazio')
            #self.tmux.roskill('state_pub_robot')
            time.sleep(1)
            self.tmux.killall(self.wsocial)
            time.sleep(1)
            if check_robot():
                self.tmux.cmd(wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
                time.sleep(1)
            while check_robot():
                time.sleep(1)
            self.write_message('RESULT robot False')
            #self.checkStatus('robot')
        # robot start/stop
        elif (message=='sociaheadlnf_start'):
            self.tmux.cmd(self.wnet,"echo '@social' | netcat -w 1 localhost 9236")
            self.tmux.roslaunch(self.wsocial,'launch','socialheadnopantilt')
            self.waitfor('social',5)
            #self.waitfor('odom',1)
            #self.waitfor('sonar',1)
        elif (message=='sociaheadlnf_kill'):
            self.tmux.cmd(self.wnet,"echo '@socialkill' | netcat -w 1 localhost 9236")
            #self.tmux.roskill('orazio')
            #self.tmux.roskill('state_pub_robot')
            time.sleep(1)
            self.tmux.killall(self.wsocial)
            time.sleep(1)
            if check_robot():
                self.tmux.cmd(wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
                time.sleep(1)
            while check_robot():
                time.sleep(1)
            self.write_message('RESULT robot False')
            #self.checkStatus('robot')
        # simrobot start/stop
        elif (message[0:14]=='simrobot_start'):
            self.tmux.roslaunch(self.wrobot,'launch','simulation')
         
        elif (message=='simrobot_kill'):
            self.tmux.cmd(self.wnet,"echo '@stagekill' | netcat -w 1 localhost 9235")
            self.tmux.roskill('stageros')
            time.sleep(1)
            self.tmux.killall(self.wrobot)
            time.sleep(1)
            if check_simrobot():
                self.tmux.cmd(wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
                time.sleep(1)
            while check_simrobot():
                time.sleep(1)
            self.write_message('RESULT simrobot False')


        # wsrobot
        elif (message=='wsrobot_start'):
            self.wsrobot()
            self.checkStatus()
        elif (message=='wsrobot_kill'):
            self.tmux.cmd(self.wquit,"kill -9 `ps ax | grep websocket_robot | awk '{print $1}'`")
            time.sleep(3)
            self.checkStatus()

       
       
        

        

        elif (message=='tableok'):
            self.tmux.cmd(self.wnet,"rostopic pub -1 /ready std_msgs/String \"OK\"") 
            time.sleep(3)
            self.checkStatus('tableok')       

        # Tavoli
        
        elif (message=='face_start'):
            self.tmux.cmd(self.wplayground,'cd ~/src/social/cmd')
            self.tmux.cmd(self.wplayground,'./start_face.sh')
            #self.tmux.cmd(self.wplayground,'./start_face_fullscreen.sh')
            time.sleep(3)
            self.checkStatus('face_start')

        elif (message=='face_stop'):
            self.tmux.cmd(self.wplayground,'cd ~/src/social/cmd')
            self.tmux.cmd(self.wplayground,'./stop_face.sh')
            
            time.sleep(3)
            self.checkStatus('face_start')
        
        #elif (message=='social_start'):
        #//    self.tmux.cmd(self.wplayground,'cd ~/src/social/cmd')
        #//    self.tmux.cmd(self.wplayground,'./social_start.sh')
        #//    time.sleep(3)
        #//    self.checkStatus('social_start')

        elif (message=='face_reset'):
            self.tmux.cmd(self.wplayground,'cd ~/src/social/cmd')
            self.tmux.cmd(self.wplayground,'./face_reset.sh')
            time.sleep(3)
            self.checkStatus('creatable03')

        elif (message=='social_stop'):
            self.tmux.cmd(self.wplayground,'cd ~/src/social/cmd')
            self.tmux.cmd(self.wplayground,'./shutdown.sh < marrtino')
            time.sleep(3)
            self.checkStatus('social_stop')

        elif (message=='social_reset'):
            self.tmux.cmd(self.wplayground,'cd ~/src/social/cmd')
            self.tmux.cmd(self.wplayground,'./social_reset.sh')
            time.sleep(3)
            self.checkStatus('social_reset')

        

      
        # save map rosrun ros_waypoint_generator ros_waypoint_generator_custo
        elif (message=='save_map'):
            #self.tmux.cmd(self.wplayground,'mkdir -p ~/playground')
            self.tmux.cmd(self.wplayground,'cd ~/src/marrtino_r3d/maps')
            self.tmux.cmd(self.wplayground,'rosrun map_server map_saver -f mymap')
            self.checkStatus()
         # generazione waypoint start
        elif (message=='genwp_start'):
            #self.tmux.cmd(self.wwaypoint,'mkdir -p ~/playground')
            #self.tmux.cmd(self.wplayground,'cd ~/src/marrtino_r3d/maps')
            self.tmux.cmd(self.wwaypoint,'rosrun ros_waypoint_generator ros_waypoint_generator_custom')
            self.checkStatus()
        elif (message=='genwp_kill'):
            self.tmux.killall(self.wwaypoint)
            time.sleep(5)
            self.checkStatus()
        # generazione waypoint start
        elif (message=='genwp2_start'):
            #self.tmux.cmd(self.wwaypoint,'mkdir -p ~/playground')
            #self.tmux.cmd(self.wplayground,'cd ~/src/marrtino_r3d/maps')
            self.tmux.cmd(self.wwaypoint,'rosrun ros_waypoint_generator ros_waypoint_generator')
            self.checkStatus()
        elif (message=='genwp2_kill'):
            self.tmux.killall(self.wwaypoint)
            time.sleep(5)
            self.checkStatus()
        
      
 


        # shutdown
        elif (message=='shutdown'):
            self.tmux.quitall()
            self.checkStatus()
            self.tmux.cmd(self.wquit,'touch ~/log/shutdownrequest')
            self.tmux.cmd(self.wquit,'sudo shutdown -h now')


        else:
            print('Code received:\n%s' %message)
            if (status=='Idle'):
                t = Thread(target=run_code, args=(message,))
                t.start()
            else:
                print('Program running. This code is discarded.')



    def on_close(self):
        print('Connection closed')

    def on_ping(self, data):
        print('ping received: %s' %(data))

    def on_pong(self, data):
        print('pong received: %s' %(data))

    def check_origin(self, origin):
        #print("-- Request from %s" %(origin))
        return True


    def wsrobot(self):
        self.tmux.python(self.wwsrobot,'blockly','websocket_robot.py')
        time.sleep(3)



# Main loop (asynchrounous thread)

def main_loop(data):
    global run, websocket_server, status
    while (run):
        time.sleep(2)
        if (run and not websocket_server is None):
            try:
                websocket_server.write_message("STATUS "+status)
                #print(status)
            except tornado.websocket.WebSocketClosedError:
                # print('-- WebSocketClosedError --')
                websocket_server = None
    print("Main loop quit.")


def run_code(code):
    global status
    if (code is None):
        return





# Main program

if __name__ == "__main__":

    # Run main thread
    t = Thread(target=main_loop, args=(None,))
    t.start()

    # Run web server
    application = tornado.web.Application([
        (r'/websocketserver', MyWebSocketServer),])  
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    print("%s Websocket server listening on port %d" %(server_name,server_port))
    sys.stdout.flush()
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("-- Keyboard interrupt --")

    if (not websocket_server is None):
        websocket_server.close()
    print("%s Websocket server quit." %server_name)
    run = False    
    print("Waiting for main loop to quit...")


