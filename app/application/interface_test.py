from pytest import fixture
from .models import User, Trip
from .interface import UserInterface, TripInterface

@fixture
def user_interface() -> UserInterface:
    return UserInterface(username='Dummy', email='dummy@dummy.dm', phone_number='0600000000')

def test_UserInterface_create(user_interface: UserInterface):
    assert user_interface

def test_UserInterface_works(user_interface: UserInterface):
    user = User(**user_interface)
    assert user

@fixture
def trip_interface() -> TripInterface:
    return TripInterface(user_id=1, city_a_station_id=0, city_b_station_id=1)

def test_TripInterface_create(trip_interface: TripInterface):
    assert trip_interface

def test_TripInterface_works(trip_interface: TripInterface):
    trip = Trip(**trip_interface)
    assert trip