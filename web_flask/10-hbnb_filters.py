#!/usr/bin/python3
"""
This module starts a flask app
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


def get_sorted_states():
    """
    Returns sorted list of states with accompanying cities
    """
    # Grab all states from storage
    states = storage.all(State).values()
    # Sort all the states
    sorted_states = sorted(states, key=lambda state: state.name)
    # Sort all the cities of each state
    for state in sorted_states:
        sorted_cities = sorted(state.cities, key=lambda city: city.name)
        state.cities = sorted_cities
    return sorted_states


def get_sorted_amenities():
    """
    Returns sorted list of amenities
    """
    # Grab all amenities from storage
    amenities = storage.all(Amenity).values()
    # Sort all the amenities
    sorted_amenities = sorted(amenities, key=lambda amenity: amenity.name)
    return sorted_amenities


@app.route("/hbnb_filters", strict_slashes=False)
def get_filters():
    """
    Gets an HTML page which filters states & amenities
    """
    # Pass the sorted states and amenities to jinja template
    return render_template('10-hbnb_filters.html',
                           states=get_sorted_states(),
                           amenities=get_sorted_amenities())


@app.teardown_appcontext
def close_session(e):
    """ Close SQLAlchemy session or reload file storage session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
