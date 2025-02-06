import sqlite3
from settings import *

conn = None
cursor = None
db_name = "blog.db"

def open():
    conn = sqlite3.connect(PATH+db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()