from flaskr import app
from flask import render_template, request, redirect, url_for
from flask import render_template
import mysql.connector
from dotenv import load_dotenv
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
        samples.append({'title': row[0], 'number': row[1], 'create_day': row[2]})
        
    return render_template(
        'index.html',
        samples = samples
    )

@app.route('/form')
def form_html():
    return render_template(
        'form.html'
    )

@app.route('/regist', methods=['POST'])
def regist():
    title = request.form['title']
    number = request.form['number']
    create_day = request.form['create_day']

    connect = db_connect()
    cursor = connect.cursor()

    cursor.execute('INSERT INTO samples VALUES(%s, %s, %s) ',
                 [title, number, create_day])

    connect.commit()
    cursor.close()
    connect.close()
    return redirect(url_for('index'))
