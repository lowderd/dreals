# tests/test_models.py

import datetime

from app import db
from app.models import City, HappyHour, Restaurant, User

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
        restaurant = Restaurant(name="The Med",
                                deal="Beerz fo dayz",
                                menu="www.pornhub.com")

        # save restaurant to database
        db.session.add(restaurant)
        db.session.commit()

        self.assertEqual(Restaurant.query.count(), 1)

    def test_happy_hour_model(self):
        """
        Test number of records in Happy Hour table
        """

        # create test restaurant
        restaurant = Restaurant(name="The Med",
                                deal="Beerz fo dayz",
                                menu="www.pornhub.com")

        # save restaurant to database
        db.session.add(restaurant)
        db.session.commit()

        # create test happy hour
        happy_hour = HappyHour(day='mon',
                               restaurant_id=Restaurant.query.filter_by(name='The Med').first().id,
                               start_time=datetime.time(1, 0),
                               end_time=datetime.time(1, 30))

        # save happy hour to database
        db.session.add(happy_hour)
        db.session.commit()

        self.assertEqual(Restaurant.query.count(), 1)
