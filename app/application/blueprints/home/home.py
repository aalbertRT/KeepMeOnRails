"""Home blueprint."""

from flask import (
    Blueprint,
    flash,
    render_template,
    url_for,
    redirect,
)
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from application.models import Trip
from application.interface import TripInterface
from application.service import TripService
from application.forms import TripForm

# Blueprint configuration
home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/index/", methods=["GET", "POST"])
@login_required
def index():
    """Index page."""
    form = TripForm()
    variables = {
        "title": "Keep me on rails - Trip form",
        "sncf_token": app.config["SNCF_TOKEN"],
        "form": form,
    }
    if form.validate_on_submit():
        # Parse trip data and test existence at this date for the user
        trip_interface = TripInterface(
            user_id=current_user.id,
            departure=form.departure.data,
            arrival=form.arrival.data,
            date=form.date.data,
        )
        # Verify existence in db
        result = (
            Trip.query.filter(Trip.user_id == trip_interface["user_id"])
            .filter(Trip.date == trip_interface["date"])
            .filter(Trip.departure == trip_interface["departure"])
            .filter(Trip.arrival == trip_interface["arrival"])
            .first()
        )
        if result is None:
            TripService.create(trip_interface)
            flash("Trip request created.")
        else:
            flash("Trip request already exists.")
        return redirect(url_for("home_bp.index"))
    return render_template("trip_form.html", **variables)


@home_bp.route("/profile/", methods=["GET"])
@login_required
def profile():
    """Profile page."""
    return render_template("profile.html", user=current_user)


@home_bp.route("/dashboard/", methods=["GET"])
@login_required
def dashboard():
    """Dashboard page."""
    return render_template("dashboard.html", trips=current_user.trips)


@home_bp.route("/logout/")
@login_required
def logout():
    """User log out logic."""
    logout_user()
    return redirect(url_for("auth_bp.login"))
