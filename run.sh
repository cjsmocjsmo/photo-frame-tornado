ln -s /home/pi/Pictures/MasterPicsResize_SPLIT /home/pi/photo-frame-tornado/static/;
rm -f /home/pi/photo-frame-tornado/picinfo.db;
python3 setup.py;
python3 photoframe.py;
DISPLAY=:0 nohup firefox --kiosk http://192.168.0.26:8888/