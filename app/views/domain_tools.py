import time
from flask import jsonify, render_template
from app import app
from app.controllers.logs_controller import log_event
from app.controllers.tools_controller import whois_lookup
from app.forms import DomainToolsForm


@app.route('/tools/domains/whois', methods=['GET', 'POST'])
def whois_domain():
    definition = "WHOIS (del inglés who is, «quién es») es un protocolo TCP basado en petición/respuesta para efectuar consultas en una base de datos que permite determinar el propietario de un nombre de dominio o una dirección IP en Internet."
    start_time = time.time()
    breadcrumbs = [{
        'url': '/tools',
        'text': 'Tools'
    }, {
        'url': '/tools/domains/',
        'text': 'Dominios'
    }, {
        'url': '/tools/domains/whois',
        'text': 'WHOIS'
    }]
    form = DomainToolsForm()
    results = None
    is_results_valid = False
    if form.validate_on_submit():
        domain = form.domain.data
        results = {'whois_lookup': whois_lookup(domain)}
        
        # Debugging: Print the type and content of results['whois_lookup']
        print(f"whois_lookup result: {results['whois_lookup']}")
        print(f"type: {type(results['whois_lookup'])}")
        
        # Check if results['whois_lookup'] is a dictionary before accessing its keys
        if isinstance(results['whois_lookup'], dict):
            is_results_valid = results['whois_lookup'].get('domain_name') is not None
        else:
            # Handle the case where whois_lookup did not return a dictionary
            is_results_valid = False

    end_time = time.time()
    duration = end_time - start_time
    return render_template('tools/domains/whois.html',
                           title='WHOIS',
                           is_results_valid=is_results_valid,
                           duration=duration,
                           form=form,
                           results=results,
                           breadcrumbs=breadcrumbs,
                           definition=definition)
