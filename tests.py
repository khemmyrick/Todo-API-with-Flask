import unittest

from playhouse.test_utils import test_database
from peewee import *

import app
import config
from models import Todo, TodoDoesNotExist

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([Todo], safe=True)


class TodoModelTestCase(unittest.TestCase):
    def test_todo_creation(self):
        with test_database(TEST_DB, (Todo,)):
            Todo.create(
                name='todo1'
            )
            todo = Todo.select().get()

            self.assertEqual(
                Todo.select().count(),
                1
            )


class ViewTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()



class TodoViewsTestCase(ViewTestCase):
    def test_empty_db(self):
        with test_database(TEST_DB, (Todo,)):
            rv = self.app.get('/')
            self.assertEqual(rv.status_code, 200)

    def test_todo_create(self):
        todo_data = {
            'name': 'todo one'
        }
        with test_database(TEST_DB, (Todo,)):
            rv = self.app.post('/api/v1/todos', data=todo_data)
            self.assertEqual(rv.status_code, 201)
            self.assertEqual(rv.location, 'http://localhost/api/v1/todos/1')
            self.assertEqual(Todo.select().count(), 1)

    def test_todo_list(self):
        todo_data = {
            'name': 'todo one'
        }
        with test_database(TEST_DB, (Todo,)):
            Todo.create(**todo_data)
            rv = self.app.get('/api/v1/todos')
            self.assertIn(todo_data['name'], rv.get_data(as_text=True))

    def test_todo_delete(self):
        todo_data = {
            'name': 'todo one'
        }
        with test_database(TEST_DB, (Todo,)):
            rv1 = self.app.post('/api/v1/todos', data=todo_data)
            rv2 = self.app.delete('/api/v1/todos/1')
            self.assertEqual(rv2.status_code, 204)

    def test_todo_update(self):
        todo_data = {
            'name': 'todo one'
        }
        with test_database(TEST_DB, (Todo,)):
            rv1 = self.app.post('/api/v1/todos', data=todo_data)
            new_data = {
                'name': 'todo won'
            }
            rv2 = self.app.put('/api/v1/todos/1', data=new_data)
            self.assertEqual(rv2.status_code, 200)
            self.assertEqual(Todo.select().count(), 1)
            rv3 = self.app.get('api/v1/todos/1')
            self.assertIn('todo won', str(rv3.data))

    def test_todo_update_bad(self):
        new_data = {
            'name': 'todo won'
        }
        with test_database(TEST_DB, (Todo,)):
            rv = self.app.put('/api/v1/todos/2', data=new_data)
            self.assertRaises(TodoDoesNotExist)
            self.assertEqual(rv.status_code, 404)


if __name__ == '__main__':
    unittest.main()
