from datetime import datetime
from typing import List
from .models import db, User, Trip
from .interface import UserInterface, TripInterface


class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username: str) -> User:
        return User.query.filter(User.username == username).first()

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter(User.email == email).first()

    @staticmethod
    def update(user: User, user_changes_updates: UserInterface) -> User:
        for key in user_changes_updates.keys():
            if key == "password":
                user.set_password(user_changes_updates[key])
                continue
            setattr(user, key, user_changes_updates[key])
        db.session.commit()
        return user

    @staticmethod
    def update_last_login(user: User, last_login_date: datetime) -> User:
        setattr(user, "last_login", last_login_date)
        db.session.commit()
        return user

    @staticmethod
    def delete_by_id(user_id: int) -> List[int]:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return []
        db.session.delete(user)
        db.session.commit()
        return [user_id]

    @staticmethod
    def create(new_attrs: UserInterface) -> User:
        new_user = User(
            username=new_attrs["username"],
            email=new_attrs["email"],
            password=new_attrs["password"],
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user


class TripService:
    @staticmethod
    def get_all() -> List[Trip]:
        return Trip.query.all()

    @staticmethod
    def get_by_id(trip_id: int) -> Trip:
        return Trip.query.get(trip_id)

    @staticmethod
    def get_by_user_id(user_id: int) -> Trip:
        return Trip.query.filter(Trip.user_id == user_id).all()

    @staticmethod
    def update(trip: Trip, trip_changes_updates: TripInterface) -> Trip:
        for key in trip_changes_updates.keys():
            setattr(trip, key, trip_changes_updates[key])
        db.session.commit()
        return trip

    @staticmethod
    def delete_by_id(trip_id: int) -> List[int]:
        trip = Trip.query.filter(Trip.id == trip_id).first()
        if not trip:
            return []
        db.session.delete(trip)
        db.session.commit()
        return [trip_id]

    @staticmethod
    def create(new_attrs: TripInterface) -> Trip:
        new_trip = Trip(
            user_id=new_attrs["user_id"],
            departure=new_attrs["departure"],
            departure_id=new_attrs["departure_id"],
            arrival=new_attrs["arrival"],
            arrival_id=new_attrs["arrival_id"],
            date=new_attrs["date"],
        )
        db.session.add(new_trip)
        db.session.commit()
        return new_trip
