#!/usr/bin/python3
"""
This module starts a simple flask app
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def get_hello_hbnb():
    """ Gets the message 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def get_hbnb():
    """ Gets the message 'HBNB' """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def get_c_with_text(text):
    """ Gets C <text>, replacing underscores with spaces """
    text = text.replace('_', ' ')
    return 'C ' + text


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def get_python_with_text(text='is cool'):
    """ Gets Python <text>, replacing underscores with spaces """
    text = text.replace('_', ' ')
    return 'Python ' + text


@app.route('/number/<int:n>', strict_slashes=False)
def get_number(n):
    """ Gets '<n> is a number' only if n is an int """
    return str(n) + " is a number"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
