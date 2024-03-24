#!/bin/bash

if [ -f /etc/systemd/system/photoframeserver.service ]; then
    sudo systemctl stop photoframeserver.service;
fi

if [ -f /etc/systemd/system/photoframedisplay.service ]; then
    sudo systemctl stop photoframedisplay.service;
fi

if [ -d /usr/share/photo-frame-tornado/photo-frame-tornado ]; then
    rm -rf /usr/share/photo-frame-tornado/photo-frame-tornado/static;
    cd /usr/share/photo-frame-tornado/photo-frame-tornado;
    git pull https://github.com/cjsmocjsmo/photo-frame-tornado.git
    cd;
fi

if [ ! -L /usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT ]; then
    ln -s /home/pi/Pictures/MasterPicsResize_SPLIT /usr/share/photo-frame-tornado/photo-frame-tornado/static/;
fi

# uncomment this if you want the db to rebuild every time
# rm -f /usr/share/photo-frame-tornado/picinfo.db;

if [ ! -f /etc/systemd/system/photoframeserver.service ]; then
    sudo cp /usr/share/photo-frame-tornado/photo-frame-tornado/photoframeserver.service /etc/systemd/system/;
    sudo chmod 755 /etc/systemd/system/photoframeserver.service;
    sudo chown root:root /etc/systemd/system/photoframeserver.service;
    sudo systemctl daemon-reload;
    sudo systemctl enable photoframeserver.service;
    sudo systemctl start photoframeserver.service;
fi

if [ ! -f /etc/systemd/system/photoframedisplay.service ]; then
    sudo cp /usr/share/photo-frame-tornado/photo-frame-tornado/photoframedisplay.service /etc/systemd/system/;
    sudo chmod 755 /etc/systemd/system/photoframedisplay.service;
    sudo chown root:root /etc/systemd/system/photoframedisplay.service;
    sudo systemctl daemon-reload;
    sudo systemctl enable photoframedisplay.service;
    sudo systemctl start photoframedisplay.service;
fi