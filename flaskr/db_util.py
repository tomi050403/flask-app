from dotenv import load_dotenv
import mysql.connector
import os

def db_connect():
    """
    データベース接続関数。
    環境変数から接続情報を読み込みデータベース接続を行う。
    """
    load_dotenv()
    connection = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )
    return connection

# db_connect()