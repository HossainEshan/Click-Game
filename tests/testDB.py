from unittest import TestCase

from app import create_app, db
from app.config import TestConfig
from app.models import User

def addTestUsers():
    u1 = User(username='tom', email='tom@example.com')
    u2 = User(username='jerry', email='jerry@example.com')
    db.session.add_all([u1, u2])
    db.session.commit()


class DatabaseTests(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        addTestUsers()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_User(self):
        u = db.session.get(User, 1)
        self.assertEqual(u.username, 'tom')

    def test_Password(self):
        u = db.session.get(User, 1)
        u.set_password('milk')
        self.assertTrue(u.check_password('milk'))
        self.assertFalse(u.check_password('cheese'))