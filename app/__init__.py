from flask import Flask
import os
import api
from flask_mail import Mail
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from config import dbstring
from flask_compress import Compress


app = Flask(__name__)
db = SQLAlchemy(app)
mail = Mail(app)
Compress(app)

 
db.create.all()
app.debug = True