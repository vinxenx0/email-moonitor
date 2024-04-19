# app/controllers/main_controller.py

from flask import render_template
from app import app

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')
