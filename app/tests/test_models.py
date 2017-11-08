# tests/test_models.py

from app import db
from app.models import City, Restaurant, User

from base import TestBase


class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in User table
        """
        self.assertEqual(User.query.count(), 2)

    def test_city_model(self):
        """
        Test number of records in City table
        """

        # create test city
        city = City(name="IT", description="The IT City")

        # save city to database
        db.session.add(city)
        db.session.commit()

        self.assertEqual(City.query.count(), 1)

    def test_restaurant_model(self):
        """
        Test number of records in Restaurant table
        """

        # create test restaurant
        restaurant = Restaurant(name="CEO", description="Run the whole company")

        # save restaurant to database
        db.session.add(restaurant)
        db.session.commit()

        self.assertEqual(Restaurant.query.count(), 1)