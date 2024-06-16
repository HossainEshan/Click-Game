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

class ErrorsTestCase(unittest.TestCase):

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
    
    def test_login_error(self):
        response = self.client.post('/login', data={
            'username': 'tom',
            'password': 'cat1',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid', response.data)

        response = self.client.post('/login', data={
            'username': 'tom1',
            'password': 'cat',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid', response.data)