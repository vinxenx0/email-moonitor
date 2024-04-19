# views/user_views.py
from flask import render_template
from app import app
from app.models.user_model import User

@app.route('/usuarios')
def usuarios():
    users = User.query.all()
    return render_template('usuarios.html', users=users)
