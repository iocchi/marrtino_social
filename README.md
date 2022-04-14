# marrtino_social

# NOVNC Installation
## 
   sudo apt install x11vnc
## 
   /usr/share/novnc/utils/launch.sh --listen 8084 --vnc localhost:5900


# config env

    export MARRTINO_APPS_HOME=$HOME/src/marrtino_apps
    export MARRTINO_SOCIAL=$HOME/src/marrtino_social
    export ROS_IP=127.0.0.1
    export ROBOT_TYPE=marrtino

# Docker images

## Pre requisites

Follow instructions for installing and using [marrtino_apps](https://bitbucket.org/iocchi/marrtino_apps/src/master/docker)


## Configuration

Enable the `social` feature in `system_config.yaml`

        nano system_config.yaml

            ...

            functions:
              ...
              social: on



## Update and build

        cd $MARRTINO_APPS_HOME/docker
        ./system_update.bash

## Run

        cd $MARRTINO_APPS_HOME/docker
        ./start_docker.bash

## Quit

        cd <...>/marrtino_apps/docker
        ./stop_docker.bash


## Bringup servers

To interact with docker containers, see 
[bringup/README](https://bitbucket.org/iocchi/marrtino_apps/src/master/bringup/README.md)

## Docker access

        docker exec -it <container_name> tmux a
        docker exec 5de4af7d973a tmux a
        docker exec -it social tmux a


## Docker push

    Edit `Dockerfile.<component>` setting last docker build date

        RUN echo "<date>" > /tmp/lastdockerbuild


    Commit ang push last changes

        git commit -am "dockerhub <date>"
        git push



    Push on Docker hub (you may need to change the docker tags)

        ./docker_build.bash
        ./docker_push.bash


