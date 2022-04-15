#!/bin/sh
echo "Launch NOVNC"
# sudo apt install -y novnc x11vnc 
# ------------------------------------
x11vnc -display :0 -autoport -localhost -nopw -bg -xkb -ncache -ncache_cr -quiet -forever
/usr/share/novnc/utils/launch.sh --listen 8081 --vnc localhost:5900