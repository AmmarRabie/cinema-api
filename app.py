from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import app_secret_key, db_connection_string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
app.config['SECRET_KEY'] = app_secret_key
CORS(app)
db = SQLAlchemy(app)