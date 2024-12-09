"""
アプリケーションのテーブル初期化設定用
指定したテーブルがデータベース側になければ作成。あれば何もしない。
"""

import mysql.connector

from app_util import db_connect


def create_samples_table():
    conn = db_connect()
    cursor = conn.cursor()
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS samples (
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
