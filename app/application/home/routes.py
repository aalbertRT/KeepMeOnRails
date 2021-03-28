import json

from flask import Blueprint
from flask import render_template, request, url_for, make_response, jsonify
from flask import current_app as app

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
def ajax_request():
    input_form = json.loads(request.data)
    # 1. Test user existence
    # 2. If user exists, tests trip existence
    # 3. Otherwise, create new user and a new trip 
    print(input_form['cityA'])
    headers = {"Content-Type": "application/json"}
    return make_response(jsonify(input_form), 200, headers)