from flaskr import app
from flask import render_template

@app.route('/')
def index():
    samples = [
        {'title': 'test',
        'number': 1,
        'create_day': 20241114_2335},
        {'title': 'testtest',
        'number': 2,
        'create_day': 20241114_2337},
    ]    
    return render_template(
        'index.html',
        samples = samples
    )

