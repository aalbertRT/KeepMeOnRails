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

    def as_dict(self):
        user_dict = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "created_on": self.created_on.strftime("%Y%m%d"),
            "last_login": self.last_login.strftime("%Y%m%d"),
            "trips": [trip.as_dict() for trip in self.trips],
        }
        return user_dict

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
    arrival = db.Column(db.String, unique=False, nullable=False)
    date = db.Column(db.Date, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, unique=False, nullable=True)

    def __init__(self, user_id: int, departure: str, arrival: str, date: date):
        self.user_id = user_id
        self.departure = departure
        self.arrival = arrival
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

    def as_dict(self):
        trip_dict = {
            "id": self.id,
            "departure": self.departure,
            "arrival": self.arrival,
            "date": self.date.isoformat(),
        }
        return trip_dict

    def __str__(self):
        return "Departure: {}, Arrival: {}, date: {}".format(
            self.departure, self.arrival, self.date
        )
