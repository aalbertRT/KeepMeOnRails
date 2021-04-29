from datetime import date
from mypy_extensions import TypedDict


class UserInterface(TypedDict):
    username: str
    email: str
    password: str


class TripInterface(TypedDict):
    user_id: int
    departure: str
    departure_id: str
    arrival: str
    arrival_id: str
    date: date
