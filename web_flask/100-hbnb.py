#!/usr/bin/python3
"""
This module starts a flask app
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User

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


def get_sorted_places():
    """
    Returns sorted list of places
    """
    # Grab all places from storage
    places = storage.all(Place).values()
    # Sort all the places
    sorted_places = sorted(places, key=lambda place: place.name)

    # create the fullname of each place owner from their id
    all_users = storage.all(User).values()
    for place in sorted_places:
        for user in all_users:
            if user.id == place.user_id:
                full_name = user.first_name + " " + user.last_name
                place.owner = full_name
    return sorted_places


@app.route("/hbnb", strict_slashes=False)
def get_filters():
    """
    Gets an HTML page which filters states & amenities
    """
    # Pass the sorted states and amenities to jinja template
    return render_template('100-hbnb.html',
                           states=get_sorted_states(),
                           amenities=get_sorted_amenities(),
                           places=get_sorted_places())


@app.teardown_appcontext
def close_session(e):
    """ Close SQLAlchemy session or reload file storage session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
