# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


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
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    role = SelectField("Role", choices=[("usr", "User"), ("admin", "Administrator")])
    submit = SubmitField('Submit')
