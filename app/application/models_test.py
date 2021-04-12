from datetime import date
from pytest import fixture
from .models import User, Trip

@fixture
def user() -> User:
    return User(username='Dummy', email='dummy@dummy.dm', password='password')

def test_user_create(user: User):
    assert user

@fixture
def trip() -> Trip:
    test_date = date.fromisoformat('2021-03-30')
    return Trip(user_id=1, departure=0, arrival=1, date=test_date)

def test_trip_create(trip: Trip):
    assert trip
