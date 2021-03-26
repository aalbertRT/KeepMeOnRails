from app import db
from typing import List
from .model import User, Trip
from .interface import UserInterface, TripInterface

class UserService():
    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()
    
    @staticmethod
    def get_by_id(user_id: int) -> User:
        return User.query.get(user_id)

    @staticmethod
    def update(user: User, User_changes_updates: UserInterface) -> User:
        user.update(User_changes_updates)
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
