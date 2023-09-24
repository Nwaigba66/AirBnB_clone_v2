#!/usr/bin/python3
"""
A module that starts a simple flask app
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ Gets the simple message 'Hello HBNB!' """
    return "<h1>Hello HBNB!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
