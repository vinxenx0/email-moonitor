from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import app, db, login_manager
from app.models.user_model import User
from app.forms import LoginForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Usuario correcto.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))
    
    # Aquí está el nuevo bloque para manejar el caso del formulario no válido
    # flash('Formulario invalido', 'danger')
    return render_template('user/login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('test'))


def create_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
