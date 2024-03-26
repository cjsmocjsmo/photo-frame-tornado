#!/bin/bash

if [ -f /etc/systemd/system/photoframeserver.service ]; then
    sudo systemctl start photoframeserver.service;
fi

if [ -f /etc/systemd/system/photoframedisplay.service ]; then
    sudo systemctl start photoframedisplay.service;
fi
