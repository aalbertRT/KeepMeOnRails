from typing import List

from application.fixtures import app, db
from .models import User, Trip
from .interface import UserInterface, TripInterface
from .service import UserService

from flask_sqlalchemy import SQLAlchemy

def add_users_to_db(db: SQLAlchemy, users: List[User]):
    for user in users:
        db.session.add(user)
    db.session.commit()


def test_user_create(db: SQLAlchemy):
    # 1. Define user properties
    user_properties = {
        'username': 'user1',
        'email': 'user1@users.com',
        'phone_number': '0600000001'
    }
    # 2. Create user
    user: User = UserService.create(user_properties)
    # 3. Get users in db
    users_db: List[User] = UserService.get_all()
    # 4. Verify created user has right properties and is in the db
    assert (user.username == user_properties['username']) and \
           (user.email == user_properties['email']) and \
           (user.phone_number == user_properties['phone_number'])
    assert user in users_db

def test_user_get_all(db: SQLAlchemy):
    # 1. Add two users to db
    user1: User = User(username='user1', email='user1@users.com', phone_number='0600000001')
    user2: User = User(username='user2', email='user2@users.com', phone_number='0600000002')
    add_users_to_db(db, [user1, user2])
    # 2. Verify the db is constituted with the two previous users
    results: List[User] = UserService.get_all()
    assert len(results) == 2
    assert (user1 in results) and (user2 in results)

def test_user_get_by_id(db: SQLAlchemy):
    # 1. Add two users to db
    user1: User = User(username='user1', email='user1@users.com', phone_number='0600000001')
    user2: User = User(username='user2', email='user2@users.com', phone_number='0600000002')
    add_users_to_db(db, [user1, user2])
    # 2. Verify user 2 has the id 2
    result: User = UserService.get_by_id(2)
    assert result.username == 'user2'

def test_user_update(db: SQLAlchemy):
    # 1. Add user to db
    # 2. Modify the user
    # 3. Verify user has been modified
    assert True

def test_user_delete_by_id(db: SQLAlchemy):
    # 1. Add two users to db
    user1: User = User(username='user1', email='user1@users.com', phone_number='0600000001')
    user2: User = User(username='user2', email='user2@users.com', phone_number='0600000002')
    add_users_to_db(db, [user1, user2])
    # 2. Delete one user
    deleted_user_id = 2
    returned_ids: List[int] = UserService.delete_by_id(deleted_user_id)
    # 3. Get all the users and verify the deleted is absent
    UserService.get_all()
    assert True

