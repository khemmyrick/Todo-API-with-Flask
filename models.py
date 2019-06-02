import datetime

from argon2 import PasswordHasher
from peewee import *

DATABASE = SqliteDatabase('todos.sqlite')
HASHER = PasswordHasher()

TodoDoesNotExist = DoesNotExist

class Todo(Model):
    '''A peewee model with 3 fields. 
    
    fields:
    name is a CharField.
    completed is a BooleanField.
    created_at is a DateTimeField.
    '''
    name = CharField()
    completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Todo], safe=True)
    DATABASE.close()
