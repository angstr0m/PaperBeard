import datetime

from peewee import *

db = SqliteDatabase('./slr.sqlite')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class Protocol(BaseModel):
    questions = TextField()
    created = DateTimeField(default=datetime.datetime.now)


class Criterion(BaseModel):
    type = CharField()
    value = CharField()
    description = TextField()
    protocol = ForeignKeyField(Protocol, backref='criteria')
    connection = CharField()


class Search(BaseModel):
    term = TextField()
    platform = CharField()
    result = BlobField()
    created = DateTimeField(default=datetime.datetime.now)


class Review(BaseModel):
    name = CharField(unique=True)
    protocol = ForeignKeyField(Protocol)
    created = DateTimeField(default=datetime.datetime.now)


db.create_tables([Review, Search, Criterion, Protocol])
