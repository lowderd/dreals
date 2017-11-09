# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, URL

from ..models import City


class CityForm(FlaskForm):
    """
    Form for admin to add or edit a city
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RestaurantForm(FlaskForm):
    """
    Form for admin to add or edit a restaurant
    """
    name = StringField('Name', validators=[DataRequired()])
    city = QuerySelectField(query_factory=lambda: City.query.all(), get_label="name")
    deal = StringField('Deal', validators=[DataRequired()])
    menu = StringField('Menu Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


DAY_OPTIONS = [
        ('mon', 'Monday'),
        ('tues', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thurs', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday')
    ]


class HappyHourForm(FlaskForm):
    """
    Form for admin to add or edit a happy hour
    """
    day = SelectField("Day", choices=DAY_OPTIONS)
    start_time = DateTimeField('Start Time', display_format='%I:%M %p')
    end_time = DateTimeField('End Time', display_format='%I:%M %p')
    submit = SubmitField('submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    role = SelectField("Role", choices=[("usr", "User"), ("admin", "Administrator")])
    submit = SubmitField('Submit')
