import mysql.connector

from db_util import db_connect

def create_samples_table():
    """
    アプリケーションのテーブル初期化設定用
    指定したテーブルがmysql側になければ作成。あれば何もしない。
    """
    conn = db_connect()
    cursor = conn.cursor()
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS samples (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100),
        number INT,
        create_day DATETIME
    )
    """
    cursor.execute(create_table_sql)
    
    cursor.close()
    conn.close()
