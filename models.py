import datetime

from argon2 import PasswordHasher
from peewee import *

DATABASE = SqliteDatabase('todos.sqlite')
HASHER = PasswordHasher()

TodoDoesNotExist = DoesNotExist

class Todo(Model):
    name = CharField()
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    # DATABASE.connect(reuse_if_open=True)
    DATABASE.connect()
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
