"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.likes), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.image_url, '/static/images/default-pic.png')
        self.assertEqual(u.header_image_url, '/static/images/warbler-hero.jpg')
        self.assertEqual(u.bio, None)
        self.assertEqual(u.location, None)

    def test_user_repr(self):
        """Test is user model __repr__ functions correctly"""

        u = User(
            email"test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()

        self.assertEquals(repr(u), f'<User #{u.id}: testuser, test@test.com>')

    def test_user_signup(self):
        """Test user model signup method"""

        user = User.signup(
            email="test@test.com",
            username="testuser",
            password="password123",
            image_url = "/testimage.png"
        )
        db.session.commit()
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.username, 'testuser')
        self.assertNotEqual(user.password, 'password123')
        self.assertEqual(user.image_url, '/testimage.png')
        self.assertEqual(user.header_image_url, '/static/images/warbler-hero.jpg')
        self.assertEqual(user.bio, None)
        self.assertEqual(user.location, None)
    
    def test_user_authenticate(self):
        """Test user model authenticate method"""

        user = User.signup(
            email="test@test.com",
            username="testuser",
            password="password123",
            image_url = "/testimage.png"
        )
        db.session.commit()
        invalid_username_user = User.authenticate(username='baduser', password='password123')
        self.assertNotEqual(invalid_username_user, user)
        invalid_password_user = User.authenticate(username='testuser', password='password124')
        self.assertNotEqual(invalid_password_user, user)
        valid_user = User.authenticate(username='testuser', password='password123')
        self.assertEqual(valid_user, user)

    def test_following(self):
        """Test following methods"""

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        new_follow = Follows(user_being_followed_id=u1.id, user_following_id=u2.id)
        db.session.add(new_follow)
        db.session.commit()
        self.assertEqual(u1.is_following(u2), False)
        self.assertEqual(u2.is_following(u1), True)
        self.assertEqual(len(u1.followers), 1)
        self.assertEqual(len(u2.followers), 0)

    def test_follows(self):
        """Test follows methods"""
        
        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        new_follow = Follows(user_being_followed_id=u1.id, user_following_id=u2.id)
        db.session.add(new_follow)
        db.session.commit()
        self.assertEqual(u1.is_followed_by(u2), True)
        self.assertEqual(u2.is_followed_by(u1), False)
        self.assertEqual(len(u1.following), 0)
        self.assertEqual(len(u2.following), 1)
        
