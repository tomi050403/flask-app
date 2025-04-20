"""
アプリケーションのデータベース初期化設定用
指定したデータベースおよびテーブルがデータベース側になければ作成。あれば何もしない。
"""

from dotenv import load_dotenv
import os
import mysql.connector

from flaskr.app_util import db_connect,db_create


load_dotenv()

def get_env(env_name):
    value = os.getenv(env_name)
    if not value:
        raise ValueError(f"環境変数 '{env_name}'を設定してください")
    return value

def create_database():
    try:
        db_name = get_env("DB_NAME")
        conn = db_create()
        cursor = conn.cursor()
        create_db_sql = f"""
        CREATE DATABASE IF NOT EXISTS `{db_name}`
        """
        cursor.execute(create_db_sql)
        print(" * Database initialization completed")
    except mysql.connector.Error as err:
        print(f"データベース作成に失敗しました: {err}")
    except ValueError as ve:
        print(ve)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if  'conn' in locals():
            conn.close()

def create_samples_table():
    try:
        table_name = get_env("TABLE_NAME")
        conn = db_connect()
        cursor = conn.cursor()
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
        print(" * Table initialization completed")
    except mysql.connector.Error as err:
        print(f"テーブル作成失敗：{err}")
    except ValueError as ve:
        print(ve)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if  'conn' in locals():
            conn.close()
