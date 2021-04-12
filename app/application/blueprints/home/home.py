import json

from flask import Blueprint, flash, render_template, request, url_for, make_response, jsonify, redirect
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from application.models import User, Trip
from application.interface import UserInterface, TripInterface
from application.service import UserService, TripService
from application.forms import TripForm

# Blueprint configuration
home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    """Index page."""
    form = TripForm()
    variables = {
        'title': 'Keep me on rails - Trip form',
        'sncf_token': app.config['SNCF_TOKEN'],
        'form': form
    }
    if form.validate_on_submit():
        print('valid form')
        # Parse trip data and test existence at this date for the user
        trip_interface = TripInterface(
            user_id=current_user.id,
            departure=form.departure.data,
            arrival=form.arrival.data,
            date=form.date.data
        )
        # Verify existence in db
        result = Trip.query.filter(
            Trip.user_id==trip_interface['user_id']
        ).filter(
            Trip.date==trip_interface['date']
        ).filter(
            Trip.departure==trip_interface['departure']
        ).filter(
            Trip.arrival==trip_interface['arrival']
        ).first()
        if result is None:
            TripService.create(trip_interface)
            flash('Trip request created.')
        else:
            flash('Trip request already exists.')
        return redirect(url_for('home_bp.index'))
    return render_template('trip_form.html', **variables)

@home_bp.route('/logout/')
@login_required
def logout():
    """User log out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))