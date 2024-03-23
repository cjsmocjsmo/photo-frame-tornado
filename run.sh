if [ ! -d /usr/share/photo-frame-tornado ]; then
    sudo mkdir /usr/share/photo-frame-tornado;
    sudo chown pi:pi /usr/share/photo-frame-tornado;
    sudo chmod 755 /usr/share/photo-frame-tornado;
    cd /usr/share/photo-frame-tornado;
    git clone https://github.com/cjsmocjsmo/photo-frame-tornado.git;
fi

if [ -d /usr/share/photo-frame-tornado/photo-frame-tornado ]; then
    cd /usr/share/photo-frame-tornado/photo-frame-tornado;
    git pull;
fi

if [ ! -L /usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT ]; then
    ln -s /home/pi/Pictures/MasterPicsResize_SPLIT /usr/share/photo-frame-tornado/photo-frame-tornado/static/;
fi

# uncomment this if you want the db to rebuild every time
# rm -f /usr/share/photo-frame-tornado/picinfo.db;

if [ ! -f /etc/systemd/system/photoframeserver.service ]; then
    sudo cp /usr/share/photo-frame-tornado/photo-frame-tornado/photoframeserver.service /etc/systemd/system/;
    sudo chmod 644 /etc/systemd/system/photoframeserver.service;
    sudo chown root:root /etc/systemd/system/photoframeserver.service;
    sudo systemctl daemon-reload;
    sudo systemctl enable photoframeserver.service;
    sudo systemctl start photoframeserver.service;
fi

if [ ! -f /etc/systemd/system/photoframedisplay.service ]; then
    sudo cp /usr/share/photo-frame-tornado/photo-frame-tornado/photoframedisplay.service /etc/systemd/system/;
    sudo chmod 644 /etc/systemd/system/photoframedisplay.service;
    sudo chown root:root /etc/systemd/system/photoframedisplay.service;
    sudo systemctl daemon-reload;
    sudo systemctl enable photoframedisplay.service;
    sudo systemctl start photoframedisplay.service;
fi