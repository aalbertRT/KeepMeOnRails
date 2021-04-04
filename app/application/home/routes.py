import json

from flask import Blueprint
from flask import render_template, request, url_for, make_response, jsonify
from flask import current_app as app

from application.models import User, Trip
from application.interface import UserInterface, TripInterface
from application.service import UserService, TripService

# Blueprint configuration
home_bp = Blueprint(
    'home_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@home_bp.route('/', methods=['GET'])
def index():
    """Form page."""
    variables = {'sncf_token': app.config['SNCF_TOKEN']}
    return render_template('index.html', **variables)

@home_bp.route('/ajax/', methods=['POST'])
def add_trip():
    input_form = json.loads(request.data)
    print(input_form)
    # Parse user data
    user_interface = UserInterface(
        username=input_form['firstName'],
        email=input_form['email'],
        phone_number=input_form['phoneNumber']
        )
    # Test user existence. If it doesn't, create it
    user_result = UserService.get_by_username(user_interface['username'])
    if user_result:
        user_id = user_result.id
    else:
        new_user = UserService.create(user_interface)
        user_id = new_user.id
    # Parse trip data and test existence at this date for the user
    trip_interface = TripInterface(
        user_id=user_id,
        city_a_station_id=input_form['cityAId'],
        city_b_station_id=input_form['cityBId'],
        date=input_form['date']
    )
    trip_results = Trip.query.filter(Trip.user_id==trip_interface['user_id']).filter(Trip.date==trip_interface['date']).first()
    if trip_results:
        print("Already one trip exists at this date for this user")
    else:
        TripService.create(trip_interface)

    # Return to client
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(input_form), 200, headers)