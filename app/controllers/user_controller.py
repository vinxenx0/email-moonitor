# app/controllers/user_controller.py
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.models.user_model import User
from app.forms import LoginForm
from app.forms import RegistrationForm

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        config_data = {
            "color_primary": "#ffffff",
            "color_secondary": "#000000",
            "color_tertiary": "#0066cc",
            "web_name": "FLASKAPP",
            "logo_url": "https://web.com/asdfadsf.png"
        }
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            config=config_data  # Asignamos el valor inicial al campo config
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Registro', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #if user and user.password == form.password.data:
        if user and user.check_password(form.password.data):
            login_user(user)
            
            app.config['COLOR_PRIMARY'] = user.config.get('color_primary', app.config['COLOR_PRIMARY'])
            app.config['COLOR_SECONDARY'] = user.config.get('color_secondary', app.config['COLOR_SECONDARY'])
            app.config['COLOR_TERTIARY'] = user.config.get('color_tertiary', app.config['COLOR_TERTIARY'])
            app.config['WEB_NAME'] = user.config.get('web_name', app.config['WEB_NAME'])
            app.config['LOGO_URL'] = user.config.get('logo_url', app.config['LOGO_URL'])
                
            flash('Usuario correcto.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))
        
    # flash('Formulario invalido', 'danger')
    return render_template('user/login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    logout_user()
    app.config.from_pyfile('../instance/config.py')
    flash('Hasta la vista', 'success')
    return render_template('user/logout.html')
