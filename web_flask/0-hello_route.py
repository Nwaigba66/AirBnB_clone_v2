#!/usr/bin/python3
"""
<<<<<<< HEAD
A module that starts a simple flask app
=======
This module starts a simple flask app
>>>>>>> db6cfe83be2f82486420f1c765070ad64a074993
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ Gets the simple message 'Hello HBNB!' """
<<<<<<< HEAD
    return "<h1>Hello HBNB!</h1>"
=======
    return "Hello HBNB!"
>>>>>>> db6cfe83be2f82486420f1c765070ad64a074993


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
