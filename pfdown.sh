#!/bin/bash

if [ -f /etc/systemd/system/photoframeserver.service ]; then
    sudo systemctl stop photoframeserver.service;
fi

if [ -f /etc/systemd/system/photoframedisplay.service ]; then
    sudo systemctl stop photoframedisplay.service;
fi



# if [ ! -L /usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT ]; then
#     ln -s /home/pi/Pictures/MasterPicsResize_SPLIT /usr/share/photo-frame-tornado/photo-frame-tornado/static/;
# fi

# uncomment this if you want the db to rebuild every time
# rm -f /usr/share/photo-frame-tornado/picinfo.db;

