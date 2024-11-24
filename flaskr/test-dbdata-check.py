"""
main.pyのindex()処理のテーブル情報確認テスト用
"""

from dotenv import load_dotenv
import mysql.connector
import os

from db_util import db_connect

connect = db_connect()
cursor = connect.cursor()

cursor.execute('SELECT * FROM samples')
db_samples = cursor.fetchall()
cursor.close()
connect.close()

samples = []
for row in db_samples:
    samples.append({'id': row[0], 'title': row[1], 'number': row[2], 'create_day': row[3]})

print(samples)
