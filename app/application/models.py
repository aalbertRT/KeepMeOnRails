from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(UserMixin, db.Model):
    """Data model for user accounts."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, unique=False, nullable=True)
    # Relationship: a user can have multiple planned trips
    # It is also mandatory to add property 'user' to the Trip object 
    trips = db.relationship('Trip', backref='user', lazy=True)
    
    def __init__(self, username: str, email: str, password: str):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.created_on = datetime.now()
        self.last_login = None

    def set_password(self, password: str):
        """Create hash password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password: str):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __str__(self):
        return 'Username: {}, email: {}'.format(self.username, self.email)

    def __repr__(self):
        return '<User %r>'.format(self.username)


class Trip(db.Model):
    """Data model for recorded trips."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    city_a_station_id = db.Column(db.String, unique=False, nullable=False)
    city_b_station_id = db.Column(db.String, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=True)

    def __init__(self, user_id: int, city_a_station_id: str, city_b_station_id: str, date: datetime):
        self.user_id = user_id
        self.city_a_station_id = city_a_station_id
        self.city_b_station_id = city_b_station_id
        self.date = date
        self.created_on = datetime.now()

    def __str__(self):
        return 'City A station: {}, City B station: {}, date: {}'.format(self.city_a_station_id,
                                                                  self.city_b_station_id,
                                                                  self.date)
