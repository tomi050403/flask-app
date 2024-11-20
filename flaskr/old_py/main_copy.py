# from flaskr import app
# from flask import render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

# app = Flask(__name__)

def db_connect():
    load_dotenv()
    connetcion = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connetcion

# @app.route('/')
def index():
    connect = db_connect()
    db_users = connect.execute('SELECT * FROM users').fetchall()    
    connect.close()

    users = []
    for row in db_users:
        users.append({
            'id': row[0],
            ''
        })

    result = cursor.fetchall()
    for row in result:
        id = row[0]
        name = row[1]
        email = row[2]
        print(f"{id} {name} {email}")
    connect.close()

    # db_users = connect.execute('SELECT * FROM users').fetchall()
    # connect.close()
    # print(db_users)
    
    # samples = []
    # for row in db_samples:
    #     samples.append({'title': row[0], 'number': row[1], 'create_day': row[2]})
        
    # return render_template(
    #     'index.html',
    #     samples = samples
    # )


if __name__ == '__main__':
    index()


# @app.route('/form')
# def form_html():
#     return render_template(
#         'form.html'
#     )

# @app.route('/regist', methods=['POST'])
# def regist():
#     title = request.form['title']
#     number = request.form['number']
#     create_day = request.form['create_day']
    
#     conn = sqlite3.connect(DATABASE)
#     conn.execute('INSERT INTO samples VALUES(?, ?, ?)',
#                  [title, number, create_day])
#     conn.commit()
#     conn.close()
#     return redirect(url_for('index'))
