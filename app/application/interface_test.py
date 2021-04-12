from datetime import date
from pytest import fixture
from .models import User, Trip
from .interface import UserInterface, TripInterface

@fixture
def user_interface() -> UserInterface:
    return UserInterface(username='Dummy', email='dummy@dummy.dm', password='password')

def test_UserInterface_create(user_interface: UserInterface):
    assert user_interface

def test_UserInterface_works(user_interface: UserInterface):
    user = User(**user_interface)
    assert user

@fixture
def trip_interface() -> TripInterface:
    test_date = date.fromisoformat('2021-03-30')
    return TripInterface(user_id=1, departure=0, arrival=1, date=test_date)

def test_TripInterface_create(trip_interface: TripInterface):
    assert trip_interface

def test_TripInterface_works(trip_interface: TripInterface):
    trip = Trip(**trip_interface)
    assert trip