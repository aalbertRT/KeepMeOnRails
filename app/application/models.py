from datetime import date, datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(UserMixin, db.Model):
    """Data model for user accounts."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(200), unique=False, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, unique=False, nullable=True)
    # Relationship: a user can have multiple planned trips
    # It is also mandatory to add property 'user' to the Trip object
    trips = db.relationship("Trip", backref="user", lazy=True)

    def __init__(self, username: str, email: str, password: str):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
        self.created_on = datetime.now()
        self.last_login = None

    def set_password(self, password: str):
        """Create hash password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password: str):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __str__(self):
        return "Username: {}, email: {}".format(self.username, self.email)

    def __repr__(self):
        return "<User %r>".format(self.username)


class Trip(db.Model):
    """Data model for recorded trips."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), unique=False, nullable=False
    )
    departure = db.Column(db.String, unique=False, nullable=False)
    departure_id = db.Column(db.String, unique=False, nullable=False)
    arrival = db.Column(db.String, unique=False, nullable=False)
    arrival_id = db.Column(db.String, unique=False, nullable=False)
    date = db.Column(db.Date, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=True)

    def __init__(
        self,
        user_id: int,
        departure: str,
        departure_id: str,
        arrival: str,
        arrival_id: str,
        date: date,
    ):
        self.user_id = user_id
        self.departure = departure
        self.departure_id = departure_id
        self.arrival = arrival
        self.arrival_id = arrival_id
        self.date = date
        self.created_on = datetime.now()

    def verify_existence_in_db(self):
        result = (
            Trip.query.filter(Trip.user_id == self.user_id)
            .filter(Trip.date == self.date)
            .filter(Trip.departure == self.departure)
            .filter(Trip.arrival == self.arrival)
            .first()
        )
        if result is not None:
            return True
        return False

    def __str__(self):
        return "Departure: {}, Arrival: {}, date: {}".format(
            self.departure, self.arrival, self.date
        )
