#!/usr/bin/python3
"""
This module starts a flask app
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def display_states():
    """
    Displays an HTML page of a list of all states
    """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states, state=None)


@app.route("/states/<id>", strict_slashes=False)
def display_cities(id):
    """
    Displays an HTML page of ordered cities of a specified state
    """
    states = storage.all(State).values()

    # Search through the states for id
    for state in states:
        if id == state.id:
            # id exists and is found
            sorted_cities = sorted(state.cities, key=lambda city: city.name)
            state.cities = sorted_cities
            return render_template('9-states.html', states=None, state=state)

    # State not found
    return render_template('9-states.html', states=None, state=None)


@app.teardown_appcontext
def close_session(e):
    """ Close SQLAlchemy session or reload file storage session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
