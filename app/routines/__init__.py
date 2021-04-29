"""Routines modules."""
from operator import attrgetter
from os import environ, path
from dotenv import load_dotenv
import requests

from application.models import User, Trip
from application.service import UserService, TripService

# Load environment variables
dirname = path.dirname
basedir = path.abspath(dirname(dirname((__file__))))
load_dotenv(path.join(basedir, ".env"))


def check_trip_existence():
    """Check trip existence in SNCF catalog."""
    trips = TripService.get_all()
    for trip in sorted(trips, key=attrgetter("date")):
        trip_args = (trip.departure_id, trip.arrival_id, trip.date)
        resp = requests.get(
            "https://api.sncf.com/v1/coverage/sncf/journeys?from={}&to={}&datetime={}".format(
                *trip_args
            ),
            headers={"Authorization": environ["SNCF_TOKEN"]},
        )
        print(resp.status_code)
        resp_j = resp.json()
        # Check for journeys existence
        if "journeys" in resp_j:
            print("OK")
        else:
            print("NOK")
