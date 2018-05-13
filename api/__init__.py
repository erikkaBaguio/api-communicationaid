from flask import Flask, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import psycopg2
from flask_compress import Compress
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:walakokahibaw@localhost/db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
mail = Mail(app)
Compress(app)

from app import api

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *

db.create_all()
app.debug = True
