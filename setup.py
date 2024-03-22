import os
import sqlite3

GLOBAL_IDX = 0
GLOBAL_COUNT = 0

def set_env_vars():
  os.environ['PFPICPATH'] = '/home/pi/photo-frame-tornado/static/MasterPicsResize_SPLIT/'
  os.environ['PFDBPATH'] = '/home/pi/photo-frame-tornado/picinfo.db'
  print('Environment variables set')

def check_create_db():
  db_path = os.environ.get('PFDBPATH')
  if not os.path.exists(db_path):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    # Create the database file
    open(db_path, 'a').close()
    GLOBAL_COUNT = 0
  else:
    try:
      conn = connect_to_db()
      cursor = conn.cursor()
      cursor.execute('SELECT MAX(pfidx) FROM picinfo')
      result = cursor.fetchone()
      if result[0] is not None:
        GLOBAL_COUNT = result[0]
      else:
        GLOBAL_COUNT = 0
      conn.close()
    except sqlite3.OperationalError:
      # Create the database file
      open(db_path, 'a').close()
      GLOBAL_COUNT = 0
    print('Database checked and created')

def connect_to_db():
  db_path = os.environ.get('PFDBPATH')
  conn = sqlite3.connect(db_path)
  return conn

def create_table():
  conn = connect_to_db()
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
  
def walk_files():
  print("Starting walk_files")
  flist = []
  pic_path = os.environ.get('PFPICPATH')
  print(pic_path)
  for root, dirs, files in os.walk(pic_path):
    for file in files:
      if file.endswith('.jpg'):
        print(file)
        flist.append(os.path.join(root, file))
  print('Files walked')
  return flist
        
        
def get_file_info(filez):
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
    # Connect to the db
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''
      INSERT OR IGNORE INTO picinfo (pfidx, pfpath, pfhttp)
      VALUES (:pfidx, :pfpath, :pfhttp)
    ''', data)
    conn.commit()
    conn.close()

# def set_global_count():
#     db_path = os.environ.get('PFDBPATH')
#     conn = connect_to_db()
#     cursor = conn.cursor()
#     cursor.execute('SELECT MAX(pfidx) FROM picinfo')
#     result = cursor.fetchone()
#     GLOBAL_IDX = 0
#     GLOBAL_COUNT = 0
#     if result[0] is not None:
#         GLOBAL_COUNT = result[0]

#     data = {
#         'global_idx': GLOBAL_IDX,
#         'global_count': GLOBAL_COUNT
#     }
#     cursor.execute('''
#         INSERT INTO globals (global_idx, global_count)
#         VALUES (:global_idx, :global_count)
#     ''', data)
#     conn.commit()
#     conn.close()
#     print('Database checked and created')


        
if __name__ == '__main__':  
    print('Setting environment variables')
    set_env_vars()
    print('Checking for and creating the database')
    check_create_db()
    print('Creating the table')
    create_table()
    print('Walking the files')
    pf_files = walk_files()
    get_file_info(pf_files)
    # print('Setting the global count')
    # set_global_count()