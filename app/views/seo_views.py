import time
from flask import render_template
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
    definition = ""
    slogan = ""
    keywords = ""
    info_popup = ""
    soup = None
    response = None
    start_time = time.time()
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
        if soup:
            try:
                # Ejecutar la función correspondiente
                if tool == 'titles':
                    results = {'titles': get_page_title_issues(soup)}
                elif tool == 'titlres':
                    results = {'titles': get_page_title_issues(soup)}

            except Exception as e:
                print(f"Error processing page info: {e}")
                log_event(tool, 'Fail:' + e)
                results = {'error': e}

            if results is not None:
                log_event(tool, page)
                is_results_valid = True
            else:
                log_event(tool, 'Fail:' + page)
                results = {'error': 'Fail None results'}

        else:
                log_event(tool, 'Fail:' + page)
                results = {'error': 'Unable to parse HTML'}

    end_time = time.time()
    duration = end_time - start_time
    return render_template(
        "tools/seo/" + tool + ".html",
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
        total_checks = len(results),
        success_count = 2,
        danger_count=8,
        danger_percentage=80
    )
