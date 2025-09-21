import sqlite3
from flask import g


def last_insert_id():
    return g.last_insert_id    
    

def get_db():
    DATABASE = "database.db"
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db = g._database = sqlite3.connect(DATABASE)
    try:
        db.cursor().execute("CREATE TABLE visits (id INTEGER PRIMARY KEY, visited_at TEXT)")
    except:
        pass
    try:
        db.cursor().execute("CREATE TABLE users (id INTEGER PRIMARY KEY,username TEXT UNIQUE,password_hash TEXT)")
    except:
        pass
    try:
        db.cursor().execute("CREATE TABLE tournaments (id INTEGER PRIMARY KEY,title TEXT,description_of_event TEXT,host_id REFERENCES users,qualifier INTEGER,whenevent INTEGER)")
    except:
        pass
    return db

def execute(sql, params=[]):
    con1 = get_db()
    result = con1.execute(sql, params)
    con1.commit()
    con1.close()

def query(sql, params=[]):
    con1 = get_db()
    result = con1.cursor().execute(sql, params).fetchall()
    con1.close()
    return result