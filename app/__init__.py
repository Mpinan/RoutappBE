from flask import Flask
from app.config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
# ORM

# Psql adapter
import psycopg2
# Python OS module provides easy functions that allow us to interact and get Operating System information and even control processes up to a limit, 
# irrespective of it being a Windows Platform, Macintosh or Linux.
import os

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import models, routes