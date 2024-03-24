import os
import sqlite3
import argparse

class Setup:
    def __init__(self):
        self.global_idx = 0
        self.global_count = 0

    def set_env_vars(self):
        os.environ['PFPICPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT/'
        os.environ['PFDBPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/picinfo.db'
        print('Environment variables set')

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
        print("Starting walk_files")
        flist = []
        pic_path = os.environ.get('PFPICPATH')
        print(pic_path)
        for root, dirs, files in os.walk(pic_path):
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

    def main(self):
        print('Setting environment variables')
        self.set_env_vars()
        print('Checking for and creating the database')
        self.check_create_db()
        if self.global_count == 0:
            print('Creating the table')
            self.create_table()
            print('Walking the files')
            pf_files = self.walk_files()
            self.get_file_info(pf_files)
        else:
            print("db file exists nothing to do")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup for photo frame tornado.')
    parser.add_argument('-s', '--setup', action='store_true', help='Setup the application')
    parser.add_argument('-u', '--update', type=str, help='Update the application with a given path')
    args = parser.parse_args()

    setup = Setup()

    if args.setup:
        setup.main()
    elif args.update:
        os.environ['PFPICPATH'] = args.update
        setup.main()