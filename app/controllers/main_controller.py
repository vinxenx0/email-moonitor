# app/controllers/main_controller.py

from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app import app
from app.forms import ConfigForm

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    form = ConfigForm()
    if form.validate_on_submit():
        app.config['COLOR_PRIMARY'] = form.color_primary.data
        app.config['COLOR_SECONDARY'] = form.color_secondary.data
        app.config['COLOR_TERTIARY'] = form.color_tertiary.data
        app.config['WEB_NAME'] = form.web_name.data
        app.config['LOGO_URL'] = form.logo_url.data
        flash('Configuración actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    else:
        flash('no valida.', 'danger')
    return render_template('config.html', title='Configuración', form=form)



@app.route('/test')
def test():
    return render_template('test.html')
