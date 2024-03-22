ln -s /home/charliepi/Pictures/MasterPicsResize_SPLIT /media/charliepi/HD/photo-frame-tornado/static/;
rm -f /media/charliepi/HD/photo-frame-tornado/picinfo.db;
python3 setup.py;
python3 photoframe.py;