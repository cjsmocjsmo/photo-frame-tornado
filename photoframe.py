import os
import sqlite3
import tornado.ioloop
import tornado.web

# class Setup:
#     def __init__(self):
#         self.global_idx = 0
#         self.global_count = 0

#     def set_env_vars(self):
#         os.environ['PFPICPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT/'
#         os.environ['PFDBPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/picinfo.db'
#         print('Environment variables set')

#     def connect_to_db(self):
#         db_path = os.environ.get('PFDBPATH')
#         conn = sqlite3.connect(db_path)
#         return conn
    
#     def create_table(self):
#         conn = self.connect_to_db()
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS picinfo (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             pfidx INTEGER NOT NULL UNIQUE,
#             pfpath TEXT NOT NULL UNIQUE,
#             pfhttp TEXT NOT NULL
#             )
#         ''')
#         conn.commit()
#         conn.close()
#         print('Table created')

#     def check_create_db(self):
#         db_path = os.environ.get('PFDBPATH')
#         if not os.path.exists(db_path):
#             self.create_table()
#             self.global_count = 0
#         else:
#             try:
#                 conn = self.connect_to_db()
#                 cursor = conn.cursor()
#                 cursor.execute('SELECT MAX(pfidx) FROM picinfo')
#                 result = cursor.fetchone()
#                 if result[0] is not None:
#                     self.global_count = result[0]
#                 else:
#                     self.global_count = 0
#                 conn.close()
#             except sqlite3.OperationalError:
#                 open(db_path, 'a').close()
#                 self.global_count = 0
#             print('Database checked and created')

#     def walk_files(self):
#         print("Starting walk_files")
#         flist = []
#         pic_path = os.environ.get('PFPICPATH')
#         print(pic_path)
#         for root, dirs, files in os.walk(pic_path):
#             for file in files:
#                 if file.endswith('.jpg'):
#                     print(file)
#                     flist.append(os.path.join(root, file))
#         return flist

#     def get_file_info(self, filez):
#         idx = 0
#         for file in filez:
#             idx += 1
#             pfpath = file
#             print(idx)
#             print(pfpath)
#             dir, filet = os.path.split(file)
#             kir, folder = os.path.split(dir)
#             _, folder2 = os.path.split(kir)
#             pfhttp = os.path.join('/static/', folder2, folder, filet)
#             print(pfhttp)
#             data = {
#                 'pfidx': idx,
#                 'pfpath': pfpath,
#                 'pfhttp': pfhttp
#             }
#             conn = self.connect_to_db()
#             cursor = conn.cursor()
#             cursor.execute('''
#                 INSERT OR IGNORE INTO picinfo (pfidx, pfpath, pfhttp)
#                 VALUES (:pfidx, :pfpath, :pfhttp)
#             ''', data)
#             conn.commit()
#             conn.close()

#     def main(self):
#         print('Setting environment variables')
#         self.set_env_vars()
#         print('Checking for and creating the database')
#         self.check_create_db()
#         if self.global_count == 0:
#             print('Creating the table')
#             self.create_table()
#             print('Walking the files')
#             pf_files = self.walk_files()
#             self.get_file_info(pf_files)
#         else:
#             print("db file exists nothting to do")

# setup = Setup()
# setup.main()

GLOBAL_IDX = 0
GLOBAL_COUNT = 0

# Define the handler for the main page
class MainHandler(tornado.web.RequestHandler):
    print("Global_IDX: {}".format(GLOBAL_IDX))
    print("Global_COUNT: {}".format(GLOBAL_COUNT))
    def set_global_count(self):
        db_path = os.environ.get('PFDBPATH')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(pfidx) FROM picinfo')
        result = cursor.fetchone()
        if result[0] is not None:
            os.environ['GLOBAL_COUNT'] = str(result[0])
        conn.close()
        return str(result[0])
    
    def get_addr(self, IDX):
        print("this is IDX IDX {}".format(IDX))
        db_path = os.environ.get('PFDBPATH')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT pfhttp FROM picinfo WHERE pfidx = ?', (IDX,))
        result = cursor.fetchone()
        conn.close()
        addr = result[0]
        idx = IDX + 1
        new_idx = str(idx)
        os.environ['GLOBAL_IDX'] = new_idx
        return addr
    
    async def get(self):
        zoo = self.set_global_count()
        GLOBAL_IDX = os.environ.get('GLOBAL_IDX')
        GLOBAL_COUNT = os.environ.get('GLOBAL_COUNT')
        GLOBAL_IDX = int(GLOBAL_IDX)
        GLOBAL_COUNT = int(GLOBAL_COUNT)

        print("Global_IDX2: {}".format(GLOBAL_IDX))
        print("Global_COUNT2: {}".format(GLOBAL_COUNT))
        
        if GLOBAL_IDX == 0:
            os.environ['GLOBAL_IDX'] = '1'
            addr = "/static/MasterPicsResize_SPLIT/1/04728da2-0831-48ad-b75b-8b3cab8f9269.jpg"
            # Render the template and pass some data to it
            self.render("index.html", title="Photo Frame", addr=addr)
        elif GLOBAL_IDX <= GLOBAL_COUNT:
            addr = self.get_addr(GLOBAL_IDX)
            new_idx = GLOBAL_IDX + 1
            os.environ['GLOBAL_IDX'] = str(new_idx)
            self.render("index.html", title="Photo Frame", addr=addr)
        elif GLOBAL_IDX > GLOBAL_COUNT:
            os.environ['GLOBAL_IDX'] = '1'
            addr = "/static/MasterPicsResize_SPLIT/1/04728da2-0831-48ad-b75b-8b3cab8f9269.jpg"
            # Render the template and pass some data to it
            self.render("index.html", title="Photo Frame", addr=addr)

# Configure the application settings
settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

# Define the application routes
application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)

if __name__ == "__main__":
    # Start the Tornado server
    print("TORANDO STARTING")
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print("TORANDO STARTED")