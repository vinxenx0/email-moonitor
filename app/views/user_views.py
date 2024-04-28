# views/user_views.py
from flask import render_template
from flask_login import login_required
from app import app
from app.models.user_model import Users

@app.route('/usuarios')
@login_required
def usuarios():
    users = Users.query.all()
    return render_template('user/usuarios.html', users=users)

