import unittest
from flask import url_for
from app import create_app, db
from app.config import TestConfig
from app.models import User
import sqlalchemy as sa

def addTestUsers():
    u1 = User(username='tom', email='tom@example.com')
    u1.set_password('cat')
    u2 = User(username='jerry', email='jerry@example.com')
    u2.set_password('mouse')
    db.session.add_all([u1, u2])
    db.session.commit()

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        addTestUsers()
        self.client = self.app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
    
    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/login', data={
            'username': 'tom',
            'password': 'cat',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome tom', response.data)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Anonymous', response.data)

    def test_signup(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/signup', data={
            'username': 'spike',
            'email': 'spike@example.com',
            'password': 'dog',
            'password2': 'dog',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        
        u = db.session.get(User, 3)
        self.assertEqual('spike', u.username)
        self.assertTrue(u.check_password('dog'))
        self.assertFalse(u.check_password('bird'))