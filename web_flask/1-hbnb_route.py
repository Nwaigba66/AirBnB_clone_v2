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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
