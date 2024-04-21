# app/controllers/main_controller.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import app, db
from app.forms import ConfigForm


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
@login_required
def configuracion():
    form = ConfigForm()
    if form.validate_on_submit():
        current_user.config = {
            'color_primary': form.color_primary.data,
            'color_secondary': form.color_secondary.data,
            'color_tertiary': form.color_tertiary.data,
            'web_name': form.web_name.data,
            'logo_url': form.logo_url.data
        }
        db.session.commit()
        
        app.config['COLOR_PRIMARY'] = form.color_primary.data
        app.config['COLOR_SECONDARY'] = form.color_secondary.data
        app.config['COLOR_TERTIARY'] = form.color_tertiary.data
        app.config['WEB_NAME'] = form.web_name.data
        app.config['LOGO_URL'] = form.logo_url.data

        flash('Configuración actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        # Verificar si current_user tiene configuración antes de acceder a ella
        if current_user.config:
            form.color_primary.data = current_user.config.get('color_primary', '')
            form.color_secondary.data = current_user.config.get('color_secondary', '')
            form.color_tertiary.data = current_user.config.get('color_tertiary', '')
            form.web_name.data = current_user.config.get('web_name', '')
            form.logo_url.data = current_user.config.get('logo_url', '')
        else:
            # Si el usuario no tiene configuración, inicializar el formulario con valores vacíos
            form.color_primary.data = ''
            form.color_secondary.data = ''
            form.color_tertiary.data = ''
            form.web_name.data = ''
            form.logo_url.data = ''
    return render_template('config.html', title='Configuración', form=form)


@app.route('/test')
def test():
    return render_template('test.html')
