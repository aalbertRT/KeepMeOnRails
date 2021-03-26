from mypy_extensions import TypedDict

class UserInterface(TypedDict):
    username: str
    email: str
    phone_number: str

class TripInterface(TypedDict):
    user_id: int
    city_a_station_id: str
    city_b_station_id: str

