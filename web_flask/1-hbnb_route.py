#!/usr/bin/python3
"""A script that strats a Flask web application."""

from flask import Flask
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Route to display 'Hello HBNB!'."""
    return 'Hello HBNB!'

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Route to display 'HBNB'."""
    return 'HBNB'

if __name__ == '__main__':
    # Run the app on 0.0.0.0:5000
    app.run(host='0.0.0.0', port=5000)
