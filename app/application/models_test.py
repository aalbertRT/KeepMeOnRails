from datetime import datetime
from pytest import fixture
from .models import User, Trip

@fixture
def user() -> User:
    return User(username='Dummy', email='dummy@dummy.dm', password='password')

def test_user_create(user: User):
    assert user

@fixture
def trip() -> Trip:
    test_date = datetime.strptime('20210330', '%Y%m%d')
    return Trip(user_id=1, city_a_station_id=0, city_b_station_id=1, date=test_date)

def test_trip_create(trip: Trip):
    assert trip
