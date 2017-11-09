# project/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class City(db.Model):
    """
    Create a Cities table
    """

    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    restaurants = db.relationship('Restaurant', backref='restaurants', lazy='dynamic')

    def __repr__(self):
        return '<Cities: {}>'.format(self.name)


class Restaurant(db.Model):
    """
    Create a Restaurant table
    """

    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City')
    name = db.Column(db.String(60), unique=True)
    deal = db.Column(db.String(200))
    menu = db.Column(db.String(200))
    happy_hours = db.relationship('HappyHour', backref='happy_hours', lazy='dynamic')

    def __repr__(self):
        return '<Restaurants: {}>'.format(self.name)


class HappyHour(db.Model):
    """
    Create Happy Hour table
    """

    __tablename__ = 'happy_hours'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('Restaurant')
    day = db.Column(db.String(10))
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
