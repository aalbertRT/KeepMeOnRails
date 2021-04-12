from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.fields import HiddenField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)

class SignupForm(FlaskForm): 
    """User sign-up form"""
    name = StringField(
        'Name',
        validators=[
            Length(min=6),
            DataRequired()
        ]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm your password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """User log-in form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
    submit = SubmitField('Log In')

class TripForm(FlaskForm):
    """Trip form."""
    departure = StringField(
        'Departure',
        validators=[
            DataRequired(),
        ]
    )
    departure_id = HiddenField(
        validators=[
            DataRequired()
        ]
    )
    arrival = StringField(
        'Arrival',
        validators=[
            DataRequired(),
        ]
    )
    arrival_id = HiddenField(
        validators=[
            DataRequired()
        ]
    )
    date = DateField(
        'Trip date',
        format='%Y-%m-%d'
    )
    submit = SubmitField('Send trip request')