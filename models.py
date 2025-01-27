import peewee
from peewee import BooleanField, CharField, DateField, ForeignKeyField, TextField
from db import db, get_db

class Base(peewee.Model):
    class Meta:
        database = db

class User(Base):
    username = CharField(unique=True)
    password = CharField() # Not safe lmfao, may eventually encrypt

class Item(Base):
    name = CharField(unique=True)
    category = CharField()
    manufacturer = CharField()
    model = CharField()
    specs = TextField()
    notes = TextField()
    status = CharField()
    updated_by = ForeignKeyField(User, null=True)
    last_edited = DateField(null=True)
    # availability = BooleanField(default=True)
    loaned_by = ForeignKeyField(User, null=True, default=None)

