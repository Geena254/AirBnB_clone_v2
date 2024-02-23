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

@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """Route to display "C " followed by the value of the text variable"""
    # Replace underscores with spaces in the text variable
    text = text.replace('_', ' ')
    return 'C {}'.format(text)

@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text='is_cool'):
    """Route to display "Python " followed by the value of the text variable"""
    # Replace underscores with spaces in the text variable
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)
