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
        samples.append({
            'id': row[0],
            'title': row[1],
            'number': row[2],
            'create_day': row[3]
        })
    return render_template(
        'index.html',
        samples = samples
    )

@app.route('/create_html')
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

@app.route('/read_form/<int:sample_id>', methods=['GET'])
def read_form(sample_id):
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        """
        SELECT * FROM samples WHERE id = %s
        """,
        (sample_id,)
    )
    sample_row = cursor.fetchone()
    cursor.close()
    connect.close()
    
    if sample_row:
        sample ={
            'id': sample_row[0],
            'title': sample_row[1],
            'number': sample_row[2],
            'create_day': sample_row[3]
        }
    
    return render_template(
        'read_form.html',
        sample=sample,
        samples_id=sample_id
    )

@app.route('/update_form/<int:sample_id>', methods=['GET'])
def update_form(sample_id):
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        """
        SELECT * FROM samples WHERE id = %s
        """,
        (sample_id,)
    )
    sample_row = cursor.fetchone()
    cursor.close()
    connect.close()
    
    if sample_row:
        sample ={
            'id': sample_row[0],
            'title': sample_row[1],
            'number': sample_row[2],
            'create_day': sample_row[3]
        }
    else:
        return redirect(url_for('index'))
       
    return render_template(
        'update_form.html',
        sample=sample
    )

@app.route('/update_execute/<int:sample_id>', methods=['POST'])
def update_execute(sample_id):
    title = request.form['title']
    number = request.form['number']
    create_day = request.form['create_day']

    connect = db_connect()
    cursor = connect.cursor()
    
    cursor.execute(
        """
        UPDATE samples SET 
            title = COALESCE(NULLIF(%s, ''), title),
            number = COALESCE(NULLIF(%s, ''), number),
            create_day = COALESCE(NULLIF(%s, ''), create_day)
        WHERE id = %s
        """,
        (title, number, create_day, sample_id,)
    )
    connect.commit()
    cursor.close()
    connect.close()
    
    return redirect(url_for('update_success'))

@app.route('/update_success')
def update_success():
    return render_template(
        'update_success.html'
    )
    
    

@app.route('/delete_form/<int:sample_id>', methods=['GET','POST'])
def delete_form(sample_id):
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        """
        SELECT * FROM samples WHERE id = %s
        """,
        (sample_id,)
    )
    delete_row = cursor.fetchone()
    cursor.close()
    connect.close()

    if delete_row:
        sample ={
            'id': delete_row[0],
            'title': delete_row[1],
            'number': delete_row[2],
            'create_day': delete_row[3]
        }
   
    if request.method == 'POST':
        if 'form' in request.form:
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
        else:
            return redirect(url_for('index'))
        
    return render_template(
        'delete_form.html',
        sample=sample,
        samples_id=sample_id
    )

@app.route('/delete_success')
def delete_success_html():
    return render_template(
        'delete_success.html'
    )

@app.route('/test_html')
def test_html():
    return render_template(
        'test.html'
    )

