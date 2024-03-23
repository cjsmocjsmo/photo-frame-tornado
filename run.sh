if [ ! -L /home/pi/photo-frame-tornado/static/MasterPicsResize_SPLIT ]; then
    ln -s /home/pi/Pictures/MasterPicsResize_SPLIT /home/pi/photo-frame-tornado/static/;
fi

# rm -f /home/pi/photo-frame-tornado/picinfo.db;

if [ ! -f /etc/systemd/system/photoframeserver.service ]; then
    sudo cp /home/pi/photo-frame-tornado/photoframeserver.service /etc/systemd/system/;
    sudo chmod 644 /etc/systemd/system/photoframeserver.service;
    sudo chown root:root /etc/systemd/system/photoframeserver.service;
    sudo systemctl daemon-reload;
    sudo systemctl enable photoframeserver.service;
    sudo systemctl start photoframeserver.service;
fi

if [ ! -f /etc/systemd/system/photoframedisplay.service ]; then
    sudo cp /home/pi/photo-frame-tornado/photoframedisplay.service /etc/systemd/system/;
    sudo chmod 644 /etc/systemd/system/photoframedisplay.service;
    sudo chown root:root /etc/systemd/system/photoframedisplay.service;
    sudo systemctl daemon-reload;
    sudo systemctl enable photoframedisplay.service;
    sudo systemctl start photoframedisplay.service;
fi