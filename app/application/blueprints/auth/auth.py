from datetime import datetime

from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user

from application.models import User
from application.interface import UserInterface
from application.service import UserService
from application.forms import LoginForm, SignupForm
from application import login_manager

# Blueprint configuration
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    """Log in form page."""
    # Bypass if user logged in
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))

    form = LoginForm()
    variables = {
        'title': 'Keep me on rails - Login',
        'form': form
    }
    if form.validate_on_submit():
        user = UserService.get_by_email(form.email.data)
        # Check the user exists
        if user is not None:
            # Check password is correct
            if user.check_password(form.password.data):
                # Log in the user
                login_user(user)
                UserService.update_last_login(user, datetime.now())
                return redirect(url_for('home_bp.index'))
            flash('Invalid user/password combination.')
            return render_template('login.html', **variables)
        flash ('This email is not registered, please signup.')
        return redirect(url_for('auth_bp.signup'))
    return render_template('login.html', **variables)

@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    """Signup form page."""
    form = SignupForm()
    variables = {
        'title': 'Keep me on rails - Signup',
        'form': form
    }
    if form.validate_on_submit():
        user_interface = UserInterface(
            email = form.email.data,
            username = form.name.data,
            password = form.password.data
        )
        # Check email is not already used by an existing user
        if not UserService.get_by_email(user_interface['email']):
            new_user = UserService.create(user_interface)
            # Log in as the new user
            login_user(new_user)
            UserService.update_last_login(new_user, datetime.now())
            return redirect(url_for('home_bp.index'))
        flash('A user already exists with that email address.')
    return render_template('signup.html', **variables)

@login_manager.user_loader
def load_user(user_id):
    """On every page load, check user is logged in."""
    if user_id is not None:
        return UserService.get_by_id(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized user to Login page form."""
    flash('You muste be logged in to be on this page.')
    return redirect(url_for('auth_bp.login'))
