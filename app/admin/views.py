# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import CityForm, RestaurantForm
from .. import db
from ..models import City, Restaurant


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# City Views

@admin.route('/cities', methods=['GET', 'POST'])
@login_required
def list_cities():
    """
    List all Cities
    """
    check_admin()

    cities = City.query.all()

    return render_template('admin/cities/cities.html',
                           cities=cities, title="Cities")


@admin.route('/cities/add', methods=['GET', 'POST'])
@login_required
def add_city():
    """
    Add a City to the database
    """
    check_admin()

    add_city = True

    form = CityForm()
    if form.validate_on_submit():
        city = City(name=form.name.data,
                    description=form.description.data)
        try:
            # add City to the database
            db.session.add(city)
            db.session.commit()
            flash('You have successfully added a new city.')
        except:
            # in case City name already exists
            flash('Error: city name already exists.')

        # redirect to cities page
        return redirect(url_for('admin.list_cities'))

    # load City template
    return render_template('admin/cities/city.html', action="Add",
                           add_city=add_city, form=form,
                           title="Add City")


@admin.route('/cities/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_city(id):
    """
    Edit a City
    """
    check_admin()

    add_city = False

    city = City.query.get_or_404(id)
    form = CityForm(obj=city)
    if form.validate_on_submit():
        city.name = form.name.data
        city.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the city.')

        # redirect to the Citys page
        return redirect(url_for('admin.list_cities'))

    form.description.data = city.description
    form.name.data = city.name
    return render_template('admin/cities/city.html', action="Edit",
                           add_city=add_city, form=form,
                           city=city, title="Edit City")


@admin.route('/cities/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_city(id):
    """
    Delete a city from the database
    """
    check_admin()

    city = City.query.get_or_404(id)
    db.session.delete(city)
    db.session.commit()
    flash('You have successfully deleted the city.')

    # redirect to the cities page
    return redirect(url_for('admin.list_cities'))

    return render_template(title="Delete City")


@admin.route('/restaurants')
@login_required
def list_restaurants():
    check_admin()
    """
    List all restaurants
    """
    restaurants = Restaurant.query.all()
    return render_template('admin/restaurants/restaurants.html',
                           restaurants=restaurants, title='restaurants')


@admin.route('/restaurants/add', methods=['GET', 'POST'])
@login_required
def add_restaurant():
    """
    Add a restaurant to the database
    """
    check_admin()

    add_restaurant = True

    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(name=form.name.data,
                                description=form.description.data)

        try:
            # add restaurant to the database
            db.session.add(restaurant)
            db.session.commit()
            flash('You have successfully added a new restaurant.')
        except:
            # in case restaurant name already exists
            flash('Error: restaurant name already exists.')

        # redirect to the restaurants page
        return redirect(url_for('admin.list_restaurants'))

    # load restaurant template
    return render_template('admin/restaurants/restaurant.html', add_restaurant=add_restaurant,
                           form=form, title='Add Restaurant')


@admin.route('/restaurants/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_restaurant(id):
    """
    Edit a restaurant
    """
    check_admin()

    add_restaurant = False

    restaurant = Restaurant.query.get_or_404(id)
    form = RestaurantForm(obj=restaurant)
    if form.validate_on_submit():
        restaurant.name = form.name.data
        restaurant.description = form.description.data
        db.session.add(restaurant)
        db.session.commit()
        flash('You have successfully edited the restaurant.')

        # redirect to the restaurants page
        return redirect(url_for('admin.list_restaurants'))

    form.description.data = restaurant.description
    form.name.data = restaurant.name
    return render_template('admin/restaurants/restaurant.html', add_restaurant=add_restaurant,
                           form=form, title="Edit Restaurant")


@admin.route('/restaurants/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_restaurant(id):
    """
    Delete a restaurant from the database
    """
    check_admin()

    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    flash('You have successfully deleted the restaurant.')

    # redirect to the restaurants page
    return redirect(url_for('admin.list_restaurants'))

    return render_template(title="Delete Restaurant")

