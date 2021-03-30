from typing import List
from .models import db, User, Trip
from .interface import UserInterface, TripInterface

class UserService():
    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()
    
    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def update(user: User, user_changes_updates: UserInterface) -> User:
        for key in user_changes_updates.keys():
            setattr(user, key, user_changes_updates[key])
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
            username=new_attrs['username'],
            email=new_attrs['email'],
            phone_number=new_attrs['phone_number'],
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user


class TripService():
    @staticmethod
    def get_all() -> List[Trip]:
        return Trip.query.all()
    
    @staticmethod
    def get_by_id(trip_id: int) -> Trip:
        return Trip.query.get(trip_id)

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
            user_id=new_attrs['user_id'],
            city_a_station_id=new_attrs['city_a_station_id'],
            city_b_station_id=new_attrs['city_b_station_id'],
            date=new_attrs['date']
        )
        db.session.add(new_trip)
        db.session.commit()
        return new_trip