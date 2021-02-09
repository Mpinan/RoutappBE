from flask import Flask
from flask import jsonify, request, json

from app.models.models import User, Route
from app import app

import os


@app.route('/')

@app.route('/index')
def index():
    return "Hello, World!"

