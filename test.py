import unittest
from flask_login import login_user
from flask import url_for
from flask_testing import TestCase
from app import create_app, db
from app.models import User, Todolist, Task
from sqlalchemy.orm import Session
import datetime

class TestViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.client_context = self.app.test_request_context()
        self.client_context.push()

    def tearDown(self):
        self.client_context.pop()

    def test_landing_page(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_home_page(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_calendar_page(self):
        response = self.client.get('/calendar/')
        self.assertEqual(response.status_code, 200)
        
    def test_to_do_lists_page(self):
        response = self.client.get('/todolist/')
        self.assertEqual(response.status_code, 200)

    def test_create_to_do_list(self):
        user = db.session.get(User, 1)
        login_user(user)
        response = self.client.post('/todolist/', data=dict(
            title='test list'
        ))
        self.assertRedirects(response, '/todolist/')
        todolist = Todolist.query.filter_by(title='test list').first()
        self.assertIsNotNone(todolist)

    def test_doc(self):
        todolist = Todolist.query.filter_by(title='My List').first()
        response = self.client.get(f'/todolist/{todolist.title}/')
        context = response.get_json()
        self.assertEqual(response.status_code, 302)
        self.assertIn('to_do_list', context)
        self.assertIsInstance(context['to_do_list'], Todolist)
        self.assertIn('tasks', context)
        self.assertIsInstance(context['tasks'], list)
            
        response = self.client.post(f'/todolist/{todolist.title}/', data={'text': 'New Task'})
        self.assertRedirects(response, f'/todolist/{todolist.title}/')
        task = Task.query.filter_by(todolist=todolist.id, text='New Task').first()
        self.assertIsNone(task)


    def test_update_task(self): 
        user = db.session.get(User, 1)
        login_user(user)
        todolist = Todolist(user=user.id, title='Test Todolist')
        db.session.add(todolist)
        db.session.commit()
        task = Task(todolist=todolist.id, text='Test Task')
        db.session.add(task)
        db.session.commit()
        response = self.client.post(f'/update/{todolist.title}/{task.id}/')
        self.assertEqual(response.status_code, 302)
        task = Task.query.filter_by(id=task.id).first()
        self.assertTrue(task.complete)

    def test_delete_list(self):
        user = db.session.get(User, 1)  
        login_user(user)
        todolist = Todolist(user=user.id, title="Test Todolist")
        db.session.add(todolist)
        task = Task(todolist=todolist.id, text="Test Task")
        db.session.add(task)
        db.session.commit()
        response = self.client.post(f"/delete/{todolist.id}/")
        todolist = Todolist.query.filter_by(id=todolist.id).first()
        self.assertIsNone(todolist)
        task = Task.query.filter_by(id=task.id).all()
        self.assertIsNone(task)

    def test_delete_task(self):
        user = db.session.get(User, 1)  
        login_user(user)
        todolist = Todolist(user=user.id, title="Test Todolist")
        db.session.add(todolist)
        task = Task(todolist=todolist.id, text="Test Task")
        db.session.add(task)
        db.session.commit()
        response = self.client.post(f"/delete_task/{todolist.title}/{task.id}/")
        self.assertRedirects(response, url_for('views.to_do_lists', title=todolist.title))
        task = Task.query.filter_by(id=task.id).first()
        self.assertIsNone(task)

# if __name__ == '__main__':
#     unittest.main() 