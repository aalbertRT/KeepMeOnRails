from pytest import fixture
from .models import User, Trip

@fixture
def user() -> User:
    return User(username='Dummy', email='dummy@dummy.dm', phone_number='0600000000')

def test_user_create(user: User):
    assert user

@fixture
def trip() -> Trip:
    return Trip(user_id=1, city_a_station_id=0, city_b_station_id=1)

def test_trip_create(trip: Trip):
    assert trip
