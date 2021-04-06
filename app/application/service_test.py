from typing import List

from application.fixtures import app, db
from .models import User, Trip
from .interface import UserInterface, TripInterface
from .service import UserService, TripService

from flask_sqlalchemy import SQLAlchemy

def add_users_to_db(db: SQLAlchemy, users: List[User]):
    for user in users:
        db.session.add(user)
    db.session.commit()

class TestUserService:
    USER1_INTERFACE: UserInterface = UserInterface(
        username='user1',
        email='user1@users.com',
        phone_number='0600000001'
        )
    USER2_INTERFACE: UserInterface = UserInterface(
        username='user2',
        email='user2@users.com',
        phone_number='0600000002'
        )


    def test_create(self, db: SQLAlchemy):
        # Create user
        UserService.create(self.USER1_INTERFACE)
        # Get users in db
        results: List[User] = User.query.all()
        # Verify created user has right properties and is in the db
        assert (len(results) == 1)
        for key in self.USER1_INTERFACE.keys():
            assert getattr(results[0], key) == self.USER1_INTERFACE[key]


    def test_get_all(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Verify the db is constituted with the two previous users
        results: List[User] = UserService.get_all()
        assert len(results) == 2
        assert (user1 in results) and (user2 in results)


    def test_get_by_id(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Verify you get user2 with id 2
        result: User = UserService.get_by_id(2)
        for key in self.USER2_INTERFACE.keys():
            assert getattr(result, key) == self.USER2_INTERFACE[key]


    def test_get_by_username(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Get user1 by email
        result: User = UserService.get_by_email('user1@users.com')
        # Verify user1 is obtained
        assert result.username == 'user1@users.com'


    def test_get_by_email(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Get user1 by username
        result: User = UserService.get_by_username('user1')
        # Verify user1 is obtained
        assert result.username == 'user1'


    def test_update(self, db: SQLAlchemy):
        # Add user to db
        user: User = User(**self.USER1_INTERFACE)
        add_users_to_db(db, [user])
        # Modify the user
        UserService.update(user, self.USER2_INTERFACE)
        # Verify user has been modified
        result: User = User.query.all()[0]
        for key in self.USER2_INTERFACE.keys():
            assert getattr(result, key) == self.USER2_INTERFACE[key]


    def test_delete_by_id(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Delete one user
        deleted_user_id = 2
        UserService.delete_by_id(deleted_user_id)
        # Get all the users and verify the deleted is absent
        results: List[User] = User.query.all()
        assert (len(results) == 1) and (results[0].username == 'user1')


def add_trips_to_db(db: SQLAlchemy, trips: List[Trip]):
    for trip in trips:
        db.session.add(trip)
    db.session.commit()

class TestTripService:
    TRIP1_INTERFACE: TripInterface = TripInterface(
        user_id=1,
        city_a_station_id='0',
        city_b_station_id='1',
        date='20210330'
        )
    TRIP2_INTERFACE: TripInterface = TripInterface(
        user_id=2,
        city_a_station_id='2',
        city_b_station_id='3',
        date='20210401'
        )

    def test_create(self, db: SQLAlchemy):
        # Create trip
        TripService.create(self.TRIP1_INTERFACE)
        # Get trips in db
        results: List[Trip] = Trip.query.all()
        # Verify created trip has right properties and is in the db
        assert (len(results) == 1)
        for key in self.TRIP1_INTERFACE.keys():
            assert getattr(results[0], key) == self.TRIP1_INTERFACE[key]


    def test_get_all(self, db: SQLAlchemy):
        # Add two trips to db
        trip1: Trip = Trip(**self.TRIP1_INTERFACE)
        trip2: Trip = Trip(**self.TRIP2_INTERFACE)
        add_trips_to_db(db, [trip1, trip2])
        # Verify the db is constituted with the two previous trips
        results: List[Trip] = TripService.get_all()
        assert len(results) == 2
        assert (trip1 in results) and (trip2 in results)


    def test_get_by_id(self, db: SQLAlchemy):
        # Add two trips to db
        trip1: Trip = Trip(**self.TRIP1_INTERFACE)
        trip2: Trip = Trip(**self.TRIP2_INTERFACE)
        add_trips_to_db(db, [trip1, trip2])
        # Verify the db is constituted with the two previous trips
        result: Trip = TripService.get_by_id(2)
        for key in self.TRIP2_INTERFACE.keys():
            assert getattr(result, key) == self.TRIP2_INTERFACE[key]

    def test_get_by_user_id(self, db: SQLAlchemy):
        # Add two trips to db
        trip1: Trip = Trip(**self.TRIP1_INTERFACE)
        trip2: Trip = Trip(**self.TRIP2_INTERFACE)
        add_trips_to_db(db, [trip1, trip2])
        # Verify the db is constituted with the two previous trips
        requested_user_id = 1
        results: List[Trip] = TripService.get_by_user_id(requested_user_id)
        assert len(results) == 1
        assert results[0].user_id == requested_user_id


    def test_update(self, db: SQLAlchemy):
        # Add trip to db
        trip: Trip = Trip(**self.TRIP1_INTERFACE)
        add_trips_to_db(db, [trip])
        # Modify the trip
        TripService.update(trip, self.TRIP2_INTERFACE)
        # Verify trip has been modified
        result: Trip = Trip.query.all()[0]
        for key in self.TRIP2_INTERFACE.keys():
            assert getattr(result, key) == self.TRIP2_INTERFACE[key]


    def test_delete_by_id(self, db: SQLAlchemy):
        # Add two trips to db
        trip1: Trip = Trip(**self.TRIP1_INTERFACE)
        trip2: Trip = Trip(**self.TRIP2_INTERFACE)
        add_trips_to_db(db, [trip1, trip2])
        # Delete one trip
        deleted_trip_id = 2
        TripService.delete_by_id(deleted_trip_id)
        # Get all the trips and verify the deleted is absent
        results: List[Trip] = Trip.query.all()
        assert (len(results) == 1) and (results[0].user_id == 1)
