from flask import Flask
app = Flask(__name__)

from flaskr import main,db,app_util

try:
    db.create_database()
    db.create_samples_table()
except Exception as e:
    print(f"DB_initian_Error: {e}")
