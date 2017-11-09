# app/home/views.py

from flask import abort, render_template
from flask_login import current_user, login_required

from . import home
from ..models import City


# homepage
@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    cities = City.query.all()
    return render_template('home/index.html', cities=cities, title="Welcome")


# standard user dashboard
@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


# admin dashboard
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
