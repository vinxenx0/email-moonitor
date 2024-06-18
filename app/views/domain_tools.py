import time
from flask import render_template
from flask_login import current_user
from flask import render_template, request
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.tools_controller import *
from app.forms import DomainToolsForm
from datetime import datetime
from app.models.usage_model import Activity

##########
###
###
###
#######


@app.route("/tools/domains/<string:tool>", methods=["GET", "POST"])
def tools_domains(tool):
    definition = ""
    slogan = ""
    keywords = ""
    info_popup = ""
    start_time = time.time()
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/domains/",
            "text": "Dominios"
        },
        {
            "url": "/tools/domains/" + tool,
            "text": tool
        },
    ]
    form = DomainToolsForm()
    results = None
    is_results_valid = False

    # comprobar que existe la herramienta primero
    
    if form.validate_on_submit():
        domain = form.domain.data

        # activity

        # Obtener información del usuario
        username = 'Anonymous'
        email = ''
        if current_user.is_authenticated:
            username = current_user.username
            email = current_user.email

        url = form.domain.data  # arreglar esto
        ip_address = request.remote_addr
        user_agent = request.user_agent.string
        country = 'Spain'  #get_country_from_ip(ip_address)
        language = request.accept_languages.best

        timestamp = datetime.utcnow()

        # Obtener URL de la página actual
        page_url = request.url

        # Guardar la información del usuario en la base de datos
        user_usage = Activity(username=username,
                              email=email,
                              target=url,
                              ip_address=ip_address,
                              user_agent=user_agent,
                              country=country,
                              language=language,
                              timestamp=timestamp,
                              page_url=page_url)
        db.session.add(user_usage)
        db.session.commit()

        _results = {
            'mx_lookup': mx_lookup(domain),
            # 'whois_lookup': whois_lookup(domain),
            'dmarc_lookup': dmarc_lookup(domain),
            'spf_lookup': spf_lookup(domain),
            'dns_lookup': dns_lookup(domain),
            # 'reverse_lookup': reverse_lookup(domain),
            'dkim_lookup': dkim_lookup(domain),
            #'aaaa_lookup': aaaa_lookup(domain),
            'srv_lookup': srv_lookup('_service', '_protocol', domain),
            'cert_lookup': cert_lookup(domain),
            'bimi_lookup': bimi_lookup(domain),
            #'ip_lookup': ip_lookup(domain),
            #'cname_lookup': cname_lookup(domain),
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
            #'traceroute': traceroute_lookup(domain),
            #'nmap': nmap_lookup(domain)
        }

        if tool == 'nmap':
            results = {'nmap': nmap_lookup(domain)}
        elif tool == 'traceroute':
            results = {'traceroute_lookup': traceroute_lookup(domain)}
        elif tool == 'aaaa':
            results = {'aaaa_lookup': aaaa_lookup(domain)}
        elif tool == 'ip':
            results = {'ip_lookup': ip_lookup(domain)}
        elif tool == 'cname':
            results = {'cname_lookup': cname_lookup(domain)}
        elif tool == 'reverse':
            results = {'reverse_lookup': reverse_lookup(domain)}
        elif tool == 'whois':
            results = {"whois_lookup": whois_lookup(domain)}
        else:
            return render_template("tools/domains/notfound.html")

        print(f"results: {results}")
        print(f"type: {type(results)}")

        #### IMPORTANTE comprobar resultados

        if results is not None:  #or results[0] is not '':
            log_event(tool, domain)
            is_results_valid = True
        else:
            log_event(tool, 'Fail:' + domain)

        #if isinstance(results["traceroute_lookup"], dict):
        #if results['traceroute_lookup']['stderr'] is not '':
        #    is_results_valid = False
        #else:
        #    is_results_valid = True
 
    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/domains/" + tool + ".html",
        title=tool,
        is_results_valid=is_results_valid,
        duration=duration,
        form=form,
        results=results,
        breadcrumbs=breadcrumbs,
        definition=definition,
        slogan=slogan,
        info_popup=info_popup,
        keywords=keywords,
    )

   
