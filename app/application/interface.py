from datetime import datetime
from mypy_extensions import TypedDict

class UserInterface(TypedDict):
    username: str
    email: str
    password: str

class TripInterface(TypedDict):
    user_id: int
    city_a_station_id: str
    city_b_station_id: str
    date: datetime
