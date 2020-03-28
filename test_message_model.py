"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Likes

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
        user = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        self.client = app.test_client()

    def test_message_model(self):
        """Test does basic message model work?"""

        msg = Message(
            text="test_text",
            user_id=self.user_id
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(msg.text, 'test_text')
        self.assertEqual(msg.user_id, self.user_id)
        self.assertNotEqual(msg.id, None)
        self.assertNotEqual(msg.timestamp, None)

    def test_user_messages(self):
        """Test does message add to correct user's message count?"""
        user1 = User.query.get(self.user_id)
        msg = Message(
            text="test_text",
            user_id=user1.id
        )

        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(user1.messages), 1)

    def test_message_likes(self):
        """Test does liking message add to correct user's like count?"""
        user1 = User.query.get(self.user_id)
        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        msg = Message(
            text="test_text",
            user_id=user1.id
        )
        db.session.add(user2)
        db.session.add(msg)
        db.session.commit()
        new_like = Likes(user_id = user2.id, message_id = msg.id)
        db.session.add(new_like)
        db.session.commit()

        self.assertEqual(len(user1.likes), 0)
        self.assertEqual(len(user2.likes), 1)
