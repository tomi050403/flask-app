from flask import Flask
app = Flask(__name__)

from flaskr import main
from flaskr import db
from db_util import db_connect
db.create_samples_table()