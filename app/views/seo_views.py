import time
from flask import render_template
import requests
from app.controllers.spider_tools import check_css_status, check_deprecated_tags, check_gzip, get_canonical_info, get_common_url_issues, get_directive_issues, get_h1_issues, get_h2_issues, get_hreflang_issues, get_meta_description_issues, get_meta_keywords_issues, get_page_title_issues, get_soup, get_structured_data_issues
from flask_login import current_user
from flask import render_template, request
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.spider_tools import *
from app.forms import SeoToolsForm
from datetime import datetime
from app.models.usage_model import Activity

from app.views.info import tool_info

##########
###
###
###
#######

@app.route("/tools/seo/<string:tool>", methods=["GET", "POST"])
def tools_seo(tool):
    start_time = time.time()
    definition = ""
    slogan = ""
    keywords = ""
    info_popup = ""
    soup = None
    response = None

    # Inicializar los contadores
    total_entries = 0
    true_count = 0
    false_count = 0
    none_or_empty_count = 0
    breadcrumbs = [
        {
            "url": "/tools",
            "text": "Tools"
        },
        {
            "url": "/tools/seo/",
            "text": "SEO"
        },
        {
            "url": "/tools/seo/" + tool,
            "text": tool
        },
    ]
    form = SeoToolsForm()
    results = None
    is_results_valid = False

    # Comprobar que existe la herramienta primero
    if tool in tool_info:
        definition = tool_info[tool]['definition']
        slogan = tool_info[tool]['slogan']
        keywords = tool_info[tool]['keywords']
        info_popup = tool_info[tool]['info_popup']
    else:
        print("no existe la herramienta")
        #return render_template("tools/seo/notfound.html")

    if form.validate_on_submit():

        page = form.domain.data

        # Obtener información del usuario
        username = 'Anonymous'
        email = ''
        if current_user.is_authenticated:
            username = current_user.username
            email = current_user.email

        url = form.domain.data
        ip_address = request.remote_addr
        user_agent = request.user_agent.string
        country = 'Spain'  # get_country_from_ip(ip_address)
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


        soup = get_soup(url)
        response = requests.get(url)
        if soup:
            try:
                # Ejecutar la función correspondiente
                if tool == 'titles':
                    results = get_page_title_issues(soup)
                        
                elif tool == 'meta-description':
                    results =  get_meta_description_issues(soup)
                       
                elif tool == 'meta-keywords':
                    results = get_meta_keywords_issues(soup)
                    
                elif tool == 'headings':
                    results = get_h1_issues(soup)
                        #{
                        # #'H1_Issues': get_h1_issues(soup),
                        #'H2_Issues': get_h2_issues(soup)
                        #}

                elif tool == 'canonicals':
                    results = get_canonical_info(soup, url, response)

                elif tool == 'directives':
                    results = get_directive_issues(soup,response)

                elif tool == 'shema-org':
                    results = get_structured_data_issues(soup)

                elif tool == 'opengraph':
                    results = {"sin hacer aun"}

                elif tool == 'hreflang':
                    results = get_hreflang_issues(soup)  

                elif tool == 'urls':
                    results = get_common_url_issues(url) 

                elif tool == 'gzip':
                    results = check_gzip(url)  

                elif tool == 'deprecated-html':
                    results = check_deprecated_tags(soup) 

                elif tool == 'css':
                    results = check_css_status(response)

                
                      

            except Exception as e:
                print(f"Error processing page info: {e}")
                log_event(tool, 'Fail:' + e)
                results = {'error': e}

            if results is not None:
                log_event(tool, page)
                is_results_valid = True

                

                # Recorrer el diccionario y contar los valores según las condiciones dadas
                for key, value in results.items():
                    total_entries += 1
                    if value is True:
                        true_count += 1
                    elif value is False:
                        false_count += 1
                    elif value is None or value == '':
                        none_or_empty_count += 1

            else:
                log_event(tool, 'Fail:' + page)
                results = {'error': 'Fail None results'}

        else:
                log_event(tool, 'Fail:' + page)
                results = {'error': 'Unable to parse HTML'}

    # añadir la info extra
    # contar los true, false, y none
    # añadir ayuda

    # Calcular el porcentaje de valores False con respecto al total
    if total_entries > 0:
        false_percentage = (false_count / total_entries) * 100
    else:
        false_percentage = 0
   
    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/seo/results_seo.html",
        # "tools/seo/" + tool + ".html",
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
        total_checks =  total_entries,
        success_count = true_count,
        empty_checks = none_or_empty_count,
        danger_count=false_count,
        danger_percentage=false_percentage
    )
