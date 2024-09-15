import os
import sqlite3
import argparse
import shutil
import subprocess
import argparse
from dotenv import load_dotenv

load_dotenv()

class Setup:
    def __init__(self):
        self.global_idx = 0
        self.global_count = 0

    def connect_to_db(self):
        db_path = os.environ.get('PFDBPATH')
        conn = sqlite3.connect(db_path)
        return conn
    
    def create_table(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS picinfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pfidx INTEGER NOT NULL UNIQUE,
            pfpath TEXT NOT NULL UNIQUE,
            pfhttp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print('Table created')

    def check_create_db(self):
        db_path = os.environ.get('PFDBPATH')
        if not os.path.exists(db_path):
            self.create_table()
            self.global_count = 0
        else:
            try:
                conn = self.connect_to_db()
                cursor = conn.cursor()
                cursor.execute('SELECT MAX(pfidx) FROM picinfo')
                result = cursor.fetchone()
                if result[0] is not None:
                    self.global_count = result[0]
                else:
                    self.global_count = 0
                conn.close()
            except sqlite3.OperationalError:
                open(db_path, 'a').close()
                self.global_count = 0
            print('Database checked and created')

    def walk_files(self):
        print("Starting walk_files function")
        flist = []
        pic_path = os.environ.get('PFPICPATH')
        print(pic_path)
        for root, dirs, files in os.walk(pic_path, followlinks=True):
            for file in files:
                if file.endswith('.jpg'):
                    print(file)
                    flist.append(os.path.join(root, file))
        return flist

    def get_file_info(self, filez):
        idx = 0
        for file in filez:
            idx += 1
            pfpath = file
            print(idx)
            print(pfpath)
            dir, filet = os.path.split(file)
            kir, folder = os.path.split(dir)
            _, folder2 = os.path.split(kir)
            pfhttp = os.path.join('/static/', folder2, folder, filet)
            print(pfhttp)
            data = {
                'pfidx': idx,
                'pfpath': pfpath,
                'pfhttp': pfhttp
            }
            conn = self.connect_to_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO picinfo (pfidx, pfpath, pfhttp)
                VALUES (:pfidx, :pfpath, :pfhttp)
            ''', data)
            conn.commit()
            conn.close()

    def place_service_file(self):
        
        if not os.path.exists("/etc/systemd/system/photoframeserver.service"):
            try:
                subprocess.run("sudo", "cp", "-pvr", "photoframeserver.service", "/etc/systemd/system/")
            except Exception as e:
                print(f"Error copying photoframeserver.service: {e}")

            try:
                subprocess.run(["sudo", "chown", "root:root", "/etc/systemd/system/photoframeserver.service"])
            except Exception as e:
                print(f"Error changing ownership of photoframeserver.service: {e}")

            try:
                subprocess.run(["sudo", "chmod", "755", "/etc/systemd/system/photoframeserver.service"])
            except Exception as e:
                print(f"Error changing permissions of photoframeserver.service: {e}")

            try:
                subprocess.run(["sudo", "systemctl", "enable", "photoframeserver"])
            except Exception as e:
                print(f"Error enabling photoframeserver: {e}")

            try:
                subprocess.run(["sudo", "systemctl", "daemon-reload"])
            except Exception as e:
                print(f"Error reloading daemon: {e}")
                
            # try:
            #     subprocess.run(["sudo", "systemctl", "start", "photoframeserver"])
            # except Exception as e:
            #     print(f"Error starting photoframeserver: {e}")
        
        if not os.path.exists("/etc/systemd/system/photoframedisplay.service"):
            try:
                subprocess.run(["sudo", "cp", "-pvr", "photoframedisplay.service", "/etc/systemd/system/"])
            except Exception as e:
                print(f"Error copying photoframedisplay.service: {e}")

            try:
                subprocess.run(["sudo", "chown", "root:root", "/etc/systemd/system/photoframedisplay.service"])
            except Exception as e:
                print(f"Error changing ownership of photoframedisplay.service: {e}")

            try:
                subprocess.run(["sudo", "chmod", "755", "/etc/systemd/system/photoframedisplay.service"])
            except Exception as e:
                print(f"Error changing permissions of photoframedisplay.service: {e}")

            try:
                subprocess.run(["sudo", "systemctl", "enable", "photoframedisplay"])
            except Exception as e:
                print(f"Error enabling photoframedisplay: {e}")

            try:
                subprocess.run(["sudo", "systemctl", "daemon-reload"])
            except Exception as e:
                print(f"Error reloading daemon: {e}")

            # try:
            #     subprocess.run(["sudo", "systemctl", "start", "photoframedisplay"])
            # except Exception as e:
            #     print(f"Error starting photoframedisplay: {e}")

    def main(self):
        print('Checking for and creating the database')
        self.check_create_db()
        if self.global_count == 0:
            print('Creating the table')
            self.create_table()
            print('Walking the files')
            pf_files = self.walk_files()
            self.get_file_info(pf_files)
            # self.place_service_file()
        else:
            print("db file exists nothing to do")

class Update:
    def __init__(self, update_path):
        self.global_idx = 0
        self.global_count = 0
        self.update_dir = update_path

    # def set_env_vars(self):
    #     os.environ['PFPICPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT/'
    #     os.environ['PFDBPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/picinfo.db'
    #     print('Environment variables set')

    def connect_to_db(self):
        db_path = os.environ.get('PFDBPATH')
        conn = sqlite3.connect(db_path)
        return conn
    
    def walk_update_dir(self):
        jpgs_to_update = []
        for root, dirs, files in os.walk(self.update_dir):
            for file in files:
                if file.endswith('.jpg'):
                    jpgs_to_update.append(os.path.join(root, file))
        return jpgs_to_update
    
    def get_global_count(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(pfidx) FROM picinfo')
        result = cursor.fetchone()
        if result[0] is not None:
            self.global_count = result[0] + 1
        conn.close()

    def update_db(self):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        for jpg in self.jpgs_to_update:
            cursor.execute('SELECT pfpath FROM picinfo WHERE pfpath = ?', (jpg,))
            result = cursor.fetchone()
            if result is None:
                pfidx = self.global_count
                pfpath = jpg
                dir, filet = os.path.split(jpg)
                kir, folder = os.path.split(dir)
                _, folder2 = os.path.split(kir)
                pfhttp = os.path.join('/static/', folder2, folder, filet)
                cursor.execute('INSERT INTO picinfo (pfpath) VALUES (?)', (jpg,))
        conn.commit()
        conn.close()

    def main(self):
        self.get_global_count()
        jpgs = self.walk_update_dir()
        self.update_db()  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup for photo frame tornado.')
    parser.add_argument('-s', '--setup', type=str, help='Setup the application with a given path')
    parser.add_argument('-u', '--update', type=str, help='Update the application with a given path')
    args = parser.parse_args()

    load_dotenv()

    os.environ["PFLINKPATH"] = args.setup
    static_path = os.getenv("PFPICPATH")

    if args.setup:
        # try:
        #     os.symlink(args.setup, static_path)
        # except FileExistsError:
        #     print("Symlink already exists")
        try:
            # os.symlink(args.setup, static_path)
            subprocess.run(["ln", "-s", args.setup, static_path])

            print(f'Symbolic link created from {args.setup} to {static_path}')
            print(f"Starting setup with path {args.setup}")
            Setup().main()
        except FileExistsError:
            print(f'Symbolic link already exists at {static_path}')
            print(f"Starting setup with path {args.setup}")
            Setup().main()
        except OSError as e:
            print(f'Error creating symbolic link: {e}')
            os._exit(1)
    elif args.update:
        Update(args.update).main()
