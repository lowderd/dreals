# tests/base.py

from flask_testing import TestCase

from app import app, db
from app.models import User


class TestBase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = User(username="admin", password="admin2016", is_admin=True)

        # create test non-admin user
        visitor = User(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(visitor)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()
