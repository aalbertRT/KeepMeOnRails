from application import create_app
from routines import check_trip_existence

app = create_app()


@app.cli.command()
def trips_routine():
    """Trips checking routine."""
    check_trip_existence()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
