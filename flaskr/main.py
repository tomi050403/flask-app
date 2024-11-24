from dotenv import load_dotenv
from flaskr import app
from flask import render_template, request, redirect, url_for
import mysql.connector
import os

from db_util import db_connect


@app.route('/')
def index():
    connect = db_connect()
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM samples')
    db_samples = cursor.fetchall()
    cursor.close()
    connect.close()
   
    samples = []
    for row in db_samples:
        samples.append({'id': row[0], 'title': row[1], 'number': row[2], 'create_day': row[3]})
    return render_template(
        'index.html',
        samples = samples
    )

@app.route('/create')
def create_html():
    """
    追加ボタンの遷移先
    """
    return render_template(
        'create.html'
    )

@app.route('/regist', methods=['POST'])
def regist():
    """
    create処理
    """
    title = request.form['title']
    number = request.form['number']
    create_day = request.form['create_day']

    connect = db_connect()
    cursor = connect.cursor()

    cursor.execute(
        """
        INSERT INTO samples (title, number, create_day)
        VALUES(%s, %s, %s)
        """,
        [title, number, create_day]
    )
    connect.commit()
    cursor.close()
    connect.close()
    return redirect(url_for('create_success_html'))

@app.route('/create_success')
def create_success_html():
    return render_template(
        'create_success.html'
    )


@app.route('/delete/<int:sample_id>', methods=['POST'])
def delete_sample(sample_id):
    connect = db_connect()
    cursor = connect.cursor()
    
    cursor.execute(
        """    
        DELETE FROM samples WHERE id = %s
        """,
        (sample_id,)
    )
    
    connect.commit()
    cursor.close()
    connect.close()
    return redirect(url_for('delete_success_html'))

@app.route('/delete_success')
def delete_success_html():
    return render_template(
        'delete_success.html'
    )




@app.route('/test')
def for_test():
    """
    画面遷移のテストページ
    """
    return render_template(
        'test.html'
    )
