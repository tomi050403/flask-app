from dotenv import load_dotenv
import mysql.connector
import os

def db_create():
    load_dotenv()
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        return connection
    except Error as e:
        print(f"DB_Create_Connection_Error: {e}")
        raise

def db_connect():
    load_dotenv()
    try:
        connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        return connection
    except Error as e:
        print(f"DB_Connection_Error: {e}")
        raise

def allow_file(filename):
    files = os.getenv('ALLOW_FILES')
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in files
