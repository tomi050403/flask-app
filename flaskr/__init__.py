from flask import Flask
app = Flask(__name__)

from flaskr import main,db,app_util
db.create_samples_table()
