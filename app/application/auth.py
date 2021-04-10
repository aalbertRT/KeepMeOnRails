from flask import Blueprint, render_template, redirect, request, url_for, flash
#from flask_login import login_required, logout_user, current_user, login_user

from .models import User
from .interface import UserInterface
from .service import UserService
from .forms import LoginForm, SignupForm 

# Blueprint configuration
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    variables = {
        'title': 'Keep me on rails - Login',
        'form': form
    }
    if form.validate_on_submit():
        user = UserService.get_by_email(form.email.data)
        if user is not None:
            if user.check_password(form.password.data):
                print("Logged in")
                return redirect(url_for('home_bp.index')) 
            flash('Invalid user/password combination.')
            return render_template('login_aa.html', **variables)
        flash ('This email is not registered, please signup.')
        return redirect(url_for('auth_bp.signup'))
    return render_template('login_aa.html', **variables)

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
        if not UserService.get_by_email(user_interface['email']):
            new_user = UserService.create(user_interface)
            return redirect(url_for('auth_bp.login'))
        flash('A user already exists with that email address.')
    return render_template('signup_aa.html', **variables)

@auth_bp.route('/logout/')
def logout():
    return 'Logout'