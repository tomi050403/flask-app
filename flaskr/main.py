from flaskr import app
from flask import render_template, request, redirect, url_for
import sqlite3

DATABASE = 'database.db'

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    db_samples = conn.execute('SELECT * FROM samples').fetchall()
    conn.close()
    
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
    
    conn = sqlite3.connect(DATABASE)
    conn.execute('INSERT INTO samples VALUES(?, ?, ?)',
                 [title, number, create_day])
    conn.commit()
    conn.close()
    return redirect(url_for('index'))