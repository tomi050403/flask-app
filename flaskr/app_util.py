from dotenv import load_dotenv
import mysql.connector
import os

def db_create():
    load_dotenv()
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return connection

def db_connect():
    load_dotenv()
    connection = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )
    return connection

def allow_file(filename):
    files = os.getenv('ALLOW_FILES')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in files
