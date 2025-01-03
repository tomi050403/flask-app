import base64
from dotenv import load_dotenv
from flask import render_template, request, redirect, url_for
import mysql.connector
import os

from flaskr import app
from flaskr.app_util import db_connect,allow_file


load_dotenv()

@app.route('/')
def index():
    table_name = get_env("TABLE_NAME")
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    db_samples = cursor.fetchall()
    cursor.close()
    connect.close()
    samples = []
    for row in db_samples:
        image_data = base64.b64encode(row[2]).decode('utf-8') if row[2] else None
        samples.append({
            'id': row[0],
            'filename': row[1],
            'image_data': f"data:image/jpeg;base64,{image_data}" if image_data else None,
            'create_day': row[3],
            'update_day': row[4],
        })
    return render_template(
        'index.html',
        samples = samples
    )

@app.route('/create_html')
def create_html():
    get_acceptfile = os.getenv('ALLOW_FILES')
    return render_template(
        'create.html',
        accept_file_types=get_acceptfile
    )

@app.route('/create', methods=['POST'])
def create():
    table_name = get_env("TABLE_NAME")
    file = request.files['image_data']
    filename = request.form['filename']
    if file and allow_file(file.filename):
        image_file = request.files['image_data']
        image_data = image_file.read() if image_file else None
        connect = db_connect()
        cursor = connect.cursor()
        cursor.execute(
            f"""
            INSERT INTO {table_name} (filename, image_data, create_day)
            VALUES(%s, %s, NOW())
            """,
            [filename, image_data]
        )
        connect.commit()
        cursor.close()
        connect.close()
        return redirect(url_for('create_success_html'))
    else:
        return "File Format NG or No Upload File", 400

@app.route('/create_success')
def create_success_html():
    return render_template(
        'create_success.html'
    )

@app.route('/read_form/<int:sample_id>', methods=['GET'])
def read_form(sample_id):
    table_name = get_env("TABLE_NAME")
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        f"""
        SELECT * FROM {table_name} WHERE id = %s
        """,
        (sample_id,)
    )
    sample_row = cursor.fetchone()
    cursor.close()
    connect.close()
    if sample_row:
        image_data = base64.b64encode(sample_row[2]).decode('utf-8') if sample_row[2] else None
        sample ={
            'id': sample_row[0],
            'filename': sample_row[1],
            'image_data': f"data:image/jpeg;base64,{image_data}" if image_data else None,
            'create_day': sample_row[3],
            'update_day': sample_row[4]
        }
    return render_template(
        'read_form.html',
        sample=sample,
        samples_id=sample_id
    )

@app.route('/update_form/<int:sample_id>', methods=['GET'])
def update_form(sample_id):
    table_name = get_env("TABLE_NAME")
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        f"""
        SELECT * FROM {table_name} WHERE id = %s
        """,
        (sample_id,)
    )
    sample_row = cursor.fetchone()
    cursor.close()
    connect.close()
    if sample_row:
        image_data = base64.b64encode(sample_row[2]).decode('utf-8') if sample_row[2] else None
        sample ={
            'id': sample_row[0],
            'filename': sample_row[1],
            'image_data': f"data:image/jpeg;base64,{image_data}" if image_data else None,
            'create_day': sample_row[3],
            'update_day': sample_row[4]
        }
    get_acceptfile = os.getenv('ALLOW_FILES')
    return render_template(
        'update_form.html',
        sample=sample,
        accept_file_types=get_acceptfile
    )

@app.route('/update_execute/<int:sample_id>', methods=['POST'])
def update_execute(sample_id):
    table_name = get_env("TABLE_NAME")
    file = request.files.get('image_data')
    filename = request.form.get('filename', '').strip()
    image_data = file.read() if file and file.filename and allow_file(file.filename) else None
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        f"""
        UPDATE {table_name} SET 
            filename = COALESCE(NULLIF(%s, ''), filename),
            image_data = COALESCE(%s, image_data),
            update_day = NOW()
        WHERE id = %s
        """,
        (filename, image_data, sample_id)
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
    table_name = get_env("TABLE_NAME")
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(
        f"""
        SELECT * FROM {table_name} WHERE id = %s
        """,
        (sample_id,)
    )
    delete_row = cursor.fetchone()
    cursor.close()
    connect.close()
    if delete_row:
        image_data = base64.b64encode(delete_row[2]).decode('utf-8') if delete_row[2] else None
        sample ={
            'id': delete_row[0],
            'filename': delete_row[1],
            'image_data': f"data:image/jpeg;base64,{image_data}" if image_data else None,
            'create_day': delete_row[3],
            'update_day': delete_row[4]
        }
    if request.method == 'POST':
        if 'form' in request.form:
            connect = db_connect()
            cursor = connect.cursor()
            cursor.execute(
                f"""    
                DELETE FROM {table_name} WHERE id = %s
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

