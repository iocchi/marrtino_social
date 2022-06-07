#!/bin/bash
date

export MARRTINO_APPS_HOME=$HOME/src/marrtino_apps
export MODIM_HOME=$HOME/src/modim
export MARRTINO_SOCIAL=$HOME/src/marrtino_social

if [ ! "$1" == "-docker" ]; then
  echo "Running inside docker container..."
#  sudo service nginx start
#  sudo service shellinabox start

  echo "IP addresses: `hostname -I`"
  echo "docker exec -it <container name>  tmux   for shell access"
  echo "sample "
  echo "docker exec -it social tmux"
  #while [ ! -f "/tmp/quitrequest" ]; do
  #  sleep 5
  #done
fi

#source $HOME/.bashrc
source $HOME/ros/catkin_ws/devel/setup.bash
#export DISPLAY=:0
#export ROBOT_TYPE=marrtino

mkdir -p $HOME/log
cd $MARRTINO_SOCIAL/bringup
python social_bringup.py &> $HOME/log/social_bringup.log  
cd $MARRTINO_SOCIAL/docker/web/public/program
python websocket_robot.py &> $HOME/log/websocket_robot.log  
#cd $MARRTINO_APPS_HOME/config
#python wsconfig.py &> $HOME/log/wsconfig.log &
#roscore
echo "Social start ........"
