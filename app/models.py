import logging as lg

from .views import app

from flask_sqlalchemy import SQLAlchemy

# Create database connection object
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(200), unique=True, nullable=False)
    # Relationship: a user can have multiple planned trips
    # It is also mandatory to add property 'user' to the Trip object 
    trips = db.relationship('Trip', backref='user', lazy=True)
    
    def __init__(self, username: str, email: str, phone_number: str):
        self.username = username
        self.email = email
        self.phone_number = phone_number
    
    def __str__(self):
        return 'Username: {}, email: {}, phone number: {}'.format(self.username,
                                                                  self.email,
                                                                  self.phone_number)

    def __repr__(self):
        return '<User %r>' % self.username
        

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city_a_station_id = db.Column(db.String, nullable=False)
    city_b_station_id = db.Column(db.String, nullable=False)

    def __init__(self, user_id: int, city_a_station_id: str, city_b_station_id: str):
        self.user_id = user_id
        self.city_a_station_id = city_a_station_id
        self.city_b_station_id = city_b_station_id


def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(username='Dummy',
                        email='dummy@dummy.dm',
                        phone_number='0600000000'))
    db.session.commit()
    lg.info('Database initialized')