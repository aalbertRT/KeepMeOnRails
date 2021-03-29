from typing import List

from application.fixtures import app, db
from .models import User
from .interface import UserInterface
from .service import UserService

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
    
    def test_user_create(self, db: SQLAlchemy):
        # Create user
        UserService.create(self.USER1_INTERFACE)
        # Get users in db
        results: List[User] = User.query.all()
        # Verify created user has right properties and is in the db
        assert (len(results) == 1)
        for key in self.USER1_INTERFACE.keys():
            assert getattr(results[0], key) == self.USER1_INTERFACE[key]


    def test_user_get_all(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Verify the db is constituted with the two previous users
        results: List[User] = UserService.get_all()
        assert len(results) == 2
        assert (user1 in results) and (user2 in results)


    def test_user_get_by_id(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # Verify the db is constituted with the two previous users
        result: User = UserService.get_by_id(2)
        for key in self.USER2_INTERFACE.keys():
            assert getattr(result, key) == self.USER2_INTERFACE[key]


    def test_user_update(self, db: SQLAlchemy):
        # Add user to db
        user: User = User(**self.USER1_INTERFACE)
        add_users_to_db(db, [user])
        # Modify the user
        UserService.update(user, self.USER2_INTERFACE)
        # Verify user has been modified
        result: User = User.query.all()[0]
        for key in self.USER2_INTERFACE.keys():
            assert getattr(result, key) == self.USER2_INTERFACE[key]


    def test_user_delete_by_id(self, db: SQLAlchemy):
        # Add two users to db
        user1: User = User(**self.USER1_INTERFACE)
        user2: User = User(**self.USER2_INTERFACE)
        add_users_to_db(db, [user1, user2])
        # 2. Delete one user
        deleted_user_id = 2
        returned_ids: List[int] = UserService.delete_by_id(deleted_user_id)
        # 3. Get all the users and verify the deleted is absent
        results: List[User] = User.query.all()
        assert (len(results) == 1) and (results[0].username == 'user1')
