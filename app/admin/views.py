# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import CityForm, HappyHourForm,  RestaurantForm, UserAssignForm
from .forms import DAY_OPTIONS
from .. import db
from ..models import City, HappyHour, Restaurant, User


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a department and a role to an user
    """
    check_admin()

    user = User.query.get_or_404(id)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        if str(form.role.data) == "admin":
            user.is_admin = True
        else:
            user.is_admin = False
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')


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

    restaurant = Restaurant()
    form = RestaurantForm()
    if form.validate_on_submit():
        form.populate_obj(restaurant)
        restaurant.city_id = form.city.data.id
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
        restaurant.city_id = form.city.data.id
        restaurant.deal = form.deal.data
        restaurant.menu = form.menu.data
        db.session.add(restaurant)
        db.session.commit()
        flash('You have successfully edited the restaurant.')

        # redirect to the restaurants page
        return redirect(url_for('admin.list_restaurants'))

    form.deal.data = restaurant.deal
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


@admin.route('/restaurants/<int:id>', methods=['GET', 'POST'])
@login_required
def list_restaurant_details(id):
    """
    List all information and Happy Hours for the Restaurant
    """
    check_admin()

    restaurant = Restaurant.query.filter_by(id=id).first()
    return render_template('admin/restaurants/details.html',
                           restaurant=restaurant, title='{0} Details'.format(restaurant.name))


@admin.route('/restaurants/restaurant/<restaurant_id>/add', methods=['GET', 'POST'])
@login_required
def add_happy_hour(restaurant_id):
    """
    Add a happy hour to a restaurant
    """
    check_admin()

    add = True

    happy_hour = HappyHour()
    form = HappyHourForm()
    if form.validate_on_submit():
        happy_hour.day = dict(DAY_OPTIONS).get(form.day.data)
        happy_hour.restaurant_id = restaurant_id
        happy_hour.start_time = form.start_time.data.time()
        happy_hour.end_time = form.end_time.data.time()
        try:
            # add happy hour to the database
            db.session.add(happy_hour)
            db.session.commit()
            flash('You have successfully added a new restaurant.')
        except IOError:
            # in case restaurant name already exists
            flash('Error: happy hour already exists.')

        # redirect to the restaurants page
        return redirect(url_for('admin.list_restaurant_details', id=restaurant_id))

    # load restaurant template
    return render_template('admin/happyhours/happyhour.html', add_happy_hour=add,
                           form=form, title='Add Happy Hour')


@admin.route('/restaurants/<int:restaurant_id>/edit/<int:happy_hour_id>', methods=['GET', 'POST'])
@login_required
def edit_happy_hour(restaurant_id, happy_hour_id):
    """
    Edit a restaurant
    """
    check_admin()

    add = False

    happy_hour = HappyHour.query.get_or_404(happy_hour_id)
    form = HappyHourForm(obj=happy_hour)
    if form.validate_on_submit():
        happy_hour.day = dict(DAY_OPTIONS).get(form.day.data)
        happy_hour.restaurant_id = restaurant_id
        happy_hour.start_time = form.start_time.data
        happy_hour.end_time = form.end_time.data
        db.session.add(happy_hour)
        db.session.commit()
        flash('You have successfully edited the restaurant.')

        # redirect to the restaurants page
        return redirect(url_for('admin.list_restaurant_details', id=restaurant_id))

    form.day = happy_hour.day
    form.start_time = happy_hour.start_time.strftime("%I:%M %p")
    form.end_time = happy_hour.end_time.strftime("%I:%M %p")
    return render_template('admin/happyhours/happyhour.html', add_happy_hour=add,
                           form=form, title="Edit Happy Hour")


@admin.route('/restaurants/<int:restaurant_id>/delete/<int:happy_hour_id>', methods=['GET', 'POST'])
@login_required
def delete_happy_hour(restaurant_id, happy_hour_id):
    """
    Delete a happy hour from the database
    """
    check_admin()

    happy_hour = HappyHour.query.get_or_404(happy_hour_id)
    db.session.delete(happy_hour)
    db.session.commit()
    flash('You have successfully deleted the restaurant.')

    # redirect to the restaurants page
    return redirect(url_for('admin.list_restaurant_details', id=restaurant_id))
