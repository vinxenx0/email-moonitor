# app/controllers/user_controller.py
import datetime
from flask import render_template, redirect, session, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from sqlalchemy import create_engine
from app import app, db, mail
from app.models.user_model import User, Log
from app.forms import LoginForm, PasswordResetRequestForm
from app.forms import NewUserRegistrationForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import RegistrationForm, PasswordResetForm, PasswordChangeForm, EditProfileForm
from flask_mail import Message


@app.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('user/profile.html', user=user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)
    if user.role == 'admin':
        can_edit = True
    else:
        can_edit = False
    form = EditProfileForm()
    if form.validate_on_submit():
        # Obtener los datos del formulario
        username = form.username.data
        password = form.password.data
        role = form.role.data
        active = form.active.data
        # Verificar si el usuario es admin y puede editar
        if can_edit:
            user.username = username
            user.set_password(password)
            user.role = role
            user.active = active
            print(user)
            db.session.commit()
            flash('Usuario editado correctamente.', 'success')
            print('Usuario editado correctamente')
            return redirect(url_for('profile'))
        else:
            flash('No tienes permisos para editar el perfil.', 'success')
            print('No tienes permisos')
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = user.username
    return render_template('user/edit_profile.html',
                           user=user,
                           form=form,
                           can_edit=can_edit)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = NewUserRegistrationForm()

    if form.validate_on_submit():
        config_data = {
            "color_primary": "#ffffff",
            "color_secondary": "#000000",
            "color_tertiary": "#0066cc",
            "web_name": form.username.data,
            "logo_url": "https://web.com/asdfadsf.png"
        }
        user = User(
            username=form.username.data,
            email=form.email.data,
            role='usuario',
            config=config_data  # Asignamos el valor inicial al campo config
        )
        user.set_password(form.password.data)
        user.token = user.get_token()
        db.session.add(user)
        db.session.commit()
        # flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        send_activation_email(user)
        flash(
            'Se ha enviado un correo electrónico de confirmación. Por favor, verifica tu cuenta.',
            'success')
        return redirect(url_for('login'))
    return render_template('user/new_user.html', title='Registro', form=form)


@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    #if current_user.role == 'admin'
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
        
        # Crear la base de datos para el usuario
        database_name = f"{form.username.data}_db.sqlite"
        engine = create_engine(f'sqlite:///../instance/{database_name}')
        db.create_all(bind=engine)

        user.database_name = database_name

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
        print(user)
        if user and user.check_password(form.password.data):
            if not user.active:
                send_activation_email(user)
                flash(
                    'Tu cuenta aún no está activada. Se ha enviado un nuevo correo electrónico de activación.',
                    'warning')
                return redirect(url_for('login'))
            login_user(user)

            # Conectar a la base de datos del usuario
            engine = create_engine(f'sqlite:///../instance/{user.database_name}_db.sqlite')
            session['database_engine'] = engine

            # Registrar el inicio de sesión del usuario en la tabla de registros
            log = Log(user_id=user.id, timestamp=datetime.datetime.utcnow())
            print(log)
            db.session.add(log)
   

            app.config['COLOR_PRIMARY'] = user.config.get(
                'color_primary', app.config['COLOR_PRIMARY'])
            app.config['COLOR_SECONDARY'] = user.config.get(
                'color_secondary', app.config['COLOR_SECONDARY'])
            app.config['COLOR_TERTIARY'] = user.config.get(
                'color_tertiary', app.config['COLOR_TERTIARY'])
            app.config['WEB_NAME'] = user.config.get('web_name',
                                                     app.config['WEB_NAME'])
            app.config['LOGO_URL'] = user.config.get('logo_url',
                                                     app.config['LOGO_URL'])

            flash('Inicio de sesión exitoso.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))

    return render_template('user/login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    app.config.from_pyfile('../instance/config.py')
    flash('Hasta la vista', 'success')
    return render_template('user/logout.html')


@app.route('/activate/<token>')
def activate(token):
    user = User.verify_token(token)
    if user:
        user.active = True
        db.session.commit()
        flash('¡Tu cuenta ha sido activada! Ya puedes iniciar sesión.',
              'success')
        return redirect(url_for('login'))
    flash('El enlace de activación es inválido o ha expirado.', 'danger')
    return redirect(url_for('login'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_token(
                expires_sec=600)  # Token válido por 10 minutos (600 segundos)
            send_password_reset_email(user, token)
            flash(
                'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.',
                'success')
            return redirect(url_for('login'))
        else:
            flash(
                'No se encontró ninguna cuenta con ese correo electrónico. Por favor, verifica tu dirección de correo electrónico.',
                'danger')
    return render_template('user/reset_password_request.html',
                           title='Recuperar contraseña',
                           form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('Tu contraseña ha sido cambiada exitosamente.', 'success')
            return redirect(url_for('index'))
        else:
            flash(
                'La contraseña antigua no es correcta. Por favor, inténtalo de nuevo.',
                'danger')
    return render_template('user/change_password.html',
                           title='Cambiar Contraseña',
                           form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if not user:
        flash(
            'El enlace de restablecimiento de contraseña es inválido o ha expirado.',
            'danger')
        return redirect(url_for('login'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(
            'Tu contraseña ha sido restablecida. Ahora puedes iniciar sesión con tu nueva contraseña.',
            'success')
        return redirect(url_for('login'))
    return render_template('user/reset_password.html',
                           title='Restablecer contraseña',
                           form=form)


def send_password_reset_email(user, token):
    msg = Message('Recuperar contraseña',
                  sender='vicente@ciberpunk.es',
                  recipients=[user.email])
    print(url_for('reset_password', token=token, _external=True))
    msg.body = f'''Para restablecer tu contraseña, visita el siguiente enlace:
{url_for('reset_password', token=token, _external=True)}

If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.

El enlace es válido por 10 minutos.


'''
    #mail.send(msg)


def send_activation_email(user):
    token = user.get_token()
    msg = Message('Confirma tu cuenta',
                  sender='vicente@ciberpunk.es',
                  recipients=[user.email])
    print(url_for('activate', token=token, _external=True))
    msg.body = f'''Para activar tu cuenta, visita el siguiente enlace:
{url_for('activate', token=token, _external=True)}

If clicking the link above doesn't work, please copy and paste the URL in a new browser window instead.

El enlace es válido por 1 hora.
'''
    #mail.send(msg)


#@app.route('/accept_cookies', methods=['POST'])
#def accept_cookies():
#    session['cookies_accepted'] = True
#    session.pop('show_cookies_modal', None)
#    return redirect(request.referrer)
