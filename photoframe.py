import os
import sqlite3
import tornado.ioloop
import tornado.web


def set_env_vars():
        os.environ['PFPICPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/static/MasterPicsResize_SPLIT/'
        os.environ['PFDBPATH'] = '/usr/share/photo-frame-tornado/photo-frame-tornado/picinfo.db'
        os.environ['GLOBAL_IDX'] = '1'
        os.environ['GLOBAL_COUNT'] = '0'
        print('Environment variables set')

set_env_vars()

GLOBAL_IDX = 1
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
        print("Global_IDX1: {}".format(GLOBAL_IDX))
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