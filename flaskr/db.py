"""
アプリケーションのデータベース初期化設定用
指定したデータベースおよびテーブルがデータベース側になければ作成。あれば何もしない。
"""

from dotenv import load_dotenv
import os
import mysql.connector

from flaskr.app_util import db_connect,db_create

def create_database():
    load_dotenv()
    db_name = os.getenv("DB_NAME")
    if not db_name:
        print("環境変数 DB_NAME を設定して下さい。")
    conn = db_create()
    cursor = conn.cursor()
    create_db_sql = f"""
    CREATE DATABASE IF NOT EXISTS `{db_name}`
    """
    try:
        cursor.execute(create_db_sql)
        print("データベースが正常に作成されました")
    except mysql.connector.Error as err:
        print(f"データベース作成に失敗しました: {err}")
    finally:
        cursor.close()
        conn.close()

def create_samples_table():
    conn = db_connect()
    cursor = conn.cursor()
    table_name = os.getenv("TABLE_NAME")
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(100),
        image_data MEDIUMBLOB,
        create_day DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_day DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
    )
    """


    cursor.execute(create_table_sql)
    cursor.close()
    conn.close()
