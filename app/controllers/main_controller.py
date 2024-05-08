# app/controllers/main_controller.py

import json
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import get_page_info
from app.forms import ConfigForm, PageInfoForm



#@app.route('/')
#def index():
#   log_event('INDEX', 'pagina raíz')
#   return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    form = PageInfoForm()
    if form.validate_on_submit():
        url = form.url.data
        data = get_page_info(url)
        print(json.dumps(data))
    return render_template('start.html', data=data, form=form)

@app.route('/app')
def dashboard():
   breadcrumbs = [
        {'url': '/app', 'text': 'Dashboard'}
    ]
   log_event('DASHBOARD', 'Portada herramienta.')
   return render_template('dashboard.html', breadcrumbs=breadcrumbs)

@app.route('/config', methods=['GET', 'POST'])
@login_required
def configuracion():
    breadcrumbs = [
        {'url': '/config', 'text': 'Config'},
    ]
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
        
        log_event('CONFIG', 'Configuración del sistema actualizada.')

        flash('Configuración actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
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
 
    log_event('CONFIG', 'Visita Configuración del sistema.')
    return render_template('config.html', title='Configuración', form=form, breadcrumbs=breadcrumbs)


@app.route('/test')
def test():
    breadcrumbs = [
        {'url': '/test', 'text': 'Test'}
    ]
    #return render_template('inc/layout.html')
    return render_template('base.html')