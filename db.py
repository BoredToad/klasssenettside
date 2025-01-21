from flask import g
from peewee import SqliteDatabase

DATABASE = "db.db"

db = SqliteDatabase(DATABASE)

def get_db() -> SqliteDatabase:
    if 'db' not in g:
        g.db = db.connect()
    return g.db # pyright: ignore

def close_db():
    if g.db is not None:
        g.pop('db').close()


