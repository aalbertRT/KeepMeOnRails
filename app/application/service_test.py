from typing import List

from application.fixtures import app, db
from .models import User, Trip
from .interface import UserInterface, TripInterface
from .service import UserService

from flask_sqlalchemy import SQLAlchemy


def test_user_get_all(db: SQLAlchemy):
    # 1. Add two users to db
    user1: User = User(username="user1", email="user1@users.com", phone_number="0600000001")
    user2: User = User(username="user2", email="user2@users.com", phone_number="0600000002")
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    # 2. Verify the db is constituted with the two previous users
    results: List[User] = UserService.get_all()
    assert len(results) == 2
    assert (user1 in results) and (user2 in results)

def test_user_get_by_id():
    assert True

def test_user_update():
    assert True

def test_user_delete_by_id():
    assert True

def test_user_create():
    assert True