#!/usr/bin/python3
"""
This module starts a flask app
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def get_cities_by_states():
    """ Displays an HTML page of ordered states with cities """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    for state in sorted_states:
        sorted_cities = sorted(state.cities, key=lambda city: city.name)
        state.cities = sorted_cities
    return render_template('8-cities_by_states.html', states=sorted_states)


@app.teardown_appcontext
def close_session(e):
    """ Close SQLAlchemy session or reload file storage session """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
