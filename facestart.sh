#!/bin/sh
DISPLAY=:0 firefox http://localhost:8080/social/marrtina.html 
DISPLAY=:0 xdotool search --sync --onlyvisible --pid $! windowactivate key F11