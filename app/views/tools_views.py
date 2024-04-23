
from flask import Flask, request, jsonify
from app import app
from app.controllers.tools_controller import *

@app.route('/check_domain/<string:domain>') #, methods=['POST'])
def check_domain(domain):
    #data = request.json
    #domain = data.get('domain')
    #domain = 'cineblog.net'

    if domain:
        results = {
            'mx_lookup': mx_lookup(domain),
            'whois_lookup': whois_lookup(domain),
            'dmarc_lookup': dmarc_lookup(domain),
            'spf_lookup': spf_lookup(domain),
            'dns_lookup': dns_lookup(domain),
            'reverse_lookup': reverse_lookup(domain),
            'dkim_lookup': dkim_lookup(domain),
            'aaaa_lookup': aaaa_lookup(domain),
            'srv_lookup': srv_lookup('_service', '_protocol', domain),
            'cert_lookup': cert_lookup(domain),
            'bimi_lookup': bimi_lookup(domain),
            'ip_lookup': ip_lookup(domain),
            'cname_lookup': cname_lookup(domain),
            'soa_lookup': soa_lookup(domain),
            'txt_lookup': txt_lookup(domain),
            'dnskey_lookup': dnskey_lookup(domain),
            'ssl_lookup': ssl_lookup(domain),
            'loc_lookup': loc_lookup(domain),
            'ipseckey_lookup': ipseckey_lookup(domain),
            'asn_lookup': asn_lookup(domain),
            'rrsig_lookup': rrsig_lookup(domain),
            'nsec_lookup': nsec_lookup(domain),
            'arin_lookup': arin_lookup(domain),
            'mta_sts_lookup': mta_sts_lookup(domain),
            'nsec3param_lookup': nsec3param_lookup(domain),
            'dns_servers_lookup': dns_servers_lookup(domain),
            'http_lookup': http_lookup(domain),
            'https_lookup': https_lookup(domain),
            'ping': ping_lookup(domain),
            'traceroute': traceroute_lookup(domain),
            'nmap': nmap_lookup(domain)
        }

        sorted_results = {key: results[key] for key in sorted(results.keys())}

        return jsonify(sorted_results)
 
    else:
        return jsonify({'error': 'Domain not provided'}), 400

import subprocess
from flask import render_template, request
from app import app
from app.forms import PingForm

@app.route('/ping', methods=['GET', 'POST'])
def ping():
    form = PingForm()
    ping_result = None
    if form.validate_on_submit():
        domain = form.domain.data
        try:
            # Ejecutar el comando de ping en el sistema operativo
            result = subprocess.run(['ping', '-c', '4', domain], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                ping_result = result.stdout
            else:
                ping_result = "No se pudo hacer ping al dominio."
        except subprocess.TimeoutExpired:
            ping_result = "El ping ha superado el tiempo de espera."
    return render_template('tools/ping.html', title='PING', form=form, ping_result=ping_result)