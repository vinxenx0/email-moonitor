import time
from flask import render_template
from app.controllers.spider_tools import *
from flask_login import current_user
from flask import render_template, request
from app import app, db
from app.controllers.logs_controller import log_event
from app.controllers.tools_controller import *
from app.forms import SeoToolsForm
from datetime import datetime
from app.models.usage_model import Activity
import app.controllers.mobile_tools

import datetime

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

        _page_info = {
                
                'Canonical_Info': get_canonical_info(soup, url, response),
                'Security_Info': get_security_info(url, response, soup),
                'Common_URL_Issues': get_common_url_issues(url),
                'Page_Title_Issues': get_page_title_issues(soup),
                'Meta_Description_Issues': get_meta_description_issues(soup),
                'Meta_Keywords_Issues': get_meta_keywords_issues(soup),
                'H1_Issues': get_h1_issues(soup),
                'H2_Issues': get_h2_issues(soup),
                'Directives_Issues': get_directive_issues(soup,response),
                'HFLang_Ref_Issues' : get_hreflang_issues(soup),
                'Schema_ORG_Issues' : get_structured_data_issues(soup),
                'Header_info' : get_header_info(url),
                'Validation_Issues': validate_html(response.content),
                'Mobile_audit_Results' : app.controllers.mobile_tools.audit_mobile_usability(url, soup),
                
                # probar velocidad con buscar en diccionario # temporal
                'Internal_Details' : #get_url_details(url_info),  # Corregido aquí 
                    {
                        'Header_Name': response.headers.get('Name', ''),
                        'Header_Value': response.headers.get('Value', ''),
                        'URL': url,
                        'Status_Code': response.status_code,
                        'Status': response.reason,
                        'Content': response.headers.get('Content-Type', ''),
                        'Size': len(response.content),
                        'Transferred': response.headers.get('Content-Length', ''),
                        'Title_1': soup.find('title').text if soup.find('title') else '',
                        'Title_1_Length': len(soup.find('title').text) if soup.find('title') else 0,
                        'h1_-_1': soup.find('h1').text if soup.find('h1') else '',
                        'h1_-_Len-1': len(soup.find('h1').text) if soup.find('h1') else 0,
                        'h2_-_1': soup.find('h2').text if soup.find('h2') else '',
                        'h2_-_Len-1': len(soup.find('h2').text) if soup.find('h2') else 0,
                        'Meta_Description_1': soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else '',
                        'Meta_Description_Length_1': len(soup.find('meta', attrs={'name': 'description'}).get('content', '')) if soup.find('meta', attrs={'name': 'description'}) else 0,
                        'Meta_Description_Pixel_Width': 0,  # Aquí necesitarías calcular la anchura en píxeles
                        'Meta_Keyword_1': soup.find('meta', attrs={'name': 'keywords'}).get('content', '') if soup.find('meta', attrs={'name': 'keywords'}) else '',
                        'Meta_Keywords_Length': len(soup.find('meta', attrs={'name': 'keywords'}).get('content', '')) if soup.find('meta', attrs={'name': 'keywords'}) else 0,
                        'Meta_Robots_1': soup.find('meta', attrs={'name': 'robots'}).get('content', '') if soup.find('meta', attrs={'name': 'robots'}) else '',
                        'X-Robots-Tag_1': response.headers.get('X-Robots-Tag', ''),
                        'Meta_Refresh_1': soup.find('meta', attrs={'http-equiv': 'refresh'}).get('content', '') if soup.find('meta', attrs={'http-equiv': 'refresh'}) else '',
                        'Canonical_Link_Element': soup.find('link', attrs={'rel': 'canonical'}).get('href', '') if soup.find('link', attrs={'rel': 'canonical'}) else '',
                        'rel="next"_1': soup.find('link', attrs={'rel': 'next'}).get('href', '') if soup.find('link', attrs={'rel': 'next'}) else '',
                        'rel="prev"_1': soup.find('link', attrs={'rel': 'prev'}).get('href', '') if soup.find('link', attrs={'rel': 'prev'}) else '',
                        'HTTP_rel="next"_1': response.headers.get('Link', '').split(';')[0].strip('<>') if response.headers.get('Link') else '',
                        'HTTP_rel="prev"_1': response.headers.get('Link', '').split(';')[0].strip('<>') if response.headers.get('Link') else '',
                        'Word_Count': len(soup.text.split()),
                        'Response_Time': response.elapsed.total_seconds() if response.elapsed else 0,
                        'h2_Occurrences': len(soup.find_all('h2')),
                        'h2-1': soup.find('h2').text if soup.find('h2') else '',
                        'h2-1_length': len(soup.find('h2').text) if soup.find('h2') else 0,
                        'h1_Occurrences': len(soup.find_all('h1')),
                        'h1-1': soup.find('h1').text if soup.find('h1') else '',
                        'h1-1_length': len(soup.find('h1').text) if soup.find('h1') else 0,
                        'meat_keywords_Occurrences': len(soup.find_all('meta', attrs={'name': 'keywords'})),
                        'Meta_Keyword_2': soup.find_all('meta', attrs={'name': 'keywords'})[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 else '',
                        'Meta_Keyword_2_length': len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 and len(soup.find_all('meta', attrs={'name': 'keywords'}))[1].get('content', '') or 0,
                        'Description_Occurrences': len(soup.find_all('meta', attrs={'name': 'description'})),
                        'Meta_Description_2': soup.find_all('meta', attrs={'name': 'description'})[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'description'})) > 1 else '',
                        'Meta_Description_2_length': len(soup.find_all('meta', attrs={'name': 'description'}))[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'description'})) > 1 else 0,
                        'title_Occurrences': len(soup.find_all('title')),
                        'Title_2': soup.find_all('title')[1].text if len(soup.find_all('title')) > 1 else '',
                        'Title_2_length': len(soup.find_all('title')[1].text) if len(soup.find_all('title')) > 1 else 0,
                        'URL_Length': len(url),
                        'Last-Modified': response.headers.get('Last-Modified', ''),
                        'Address': url,
                    },
                    
                # modulos con pestaña en menu
                'Images_Issues' : audit_image_details(url,soup),

                # ultimos checks añadidos
                'Redirect Chain': check_redirects(url),
                'Gzip Compression': check_gzip(url),
                'Page Size': check_page_size(url),
                'Deprecated HTML Tags': check_deprecated_tags(soup),
                'Friendly URL': check_friendly_url(url),
                'Favicon Implemented':  check_favicon(soup),
                'WWW Redirect': check_www_redirect(url),
                'Lazy Loading Images': check_lazy_loading(soup),
                'Google Search Display': check_google_search_display(soup),
                #'Responsive Images': check_responsive_images(soup),
                'HTTP to HTTPS Redirect': check_http_to_https_redirect(url),
            

                # security rank
                'Days to SSL Expiry': check_ssl_expiry(url),
                'Outdated SSL/TLS': check_outdated_ssl_tls(response),
                'Certificate Name Match':  check_certificate_name(url),
                'Deprecated Encryption Algorithm': check_deprecated_encryption(url),
                #'HTTP URLs in Sitemap': check_http_in_sitemap(sitemap_url,soup) if sitemap_url else None,
                'Canonical HTTPS to HTTP': check_canonical_https_to_http(url,soup),
                'HTTPS to HTTP Redirect': check_https_to_http_redirect(url),
                'Mixed Content': check_mixed_content(response),

                # crawling
                #'Large Sitemap': check_large_xml_sitemap(sitemap_url_response) if sitemap_url else None,
                #'Non-Canonical Pages in Sitemap': check_non_canonical_pages_in_sitemap(sitemap_url) if sitemap_url else None,
                #'Noindex Pages in Sitemap': check_noindex_pages_in_sitemap(sitemap_url) if sitemap_url else None,
                #'Missing Sitemap': check_missing_xml_sitemap(sitemap_url) if sitemap_url else None,
                #'Sitemap in Robots.txt': check_sitemap_in_robots_txt(robots_url, sitemap_url) if robots_url and sitemap_url else None,
                #'Robots.txt Exists': check_robots_txt_exists(robots_url) if robots_url else None,
                'Frame Tag': check_frame_tag(response),
                'Long URL': check_long_url(url),
                'Noindex in HTML and HTTP': check_noindex_in_html_and_http(response),
                'Nofollow in HTML and HTTP': check_nofollow_in_html_and_http(response),
                'Canonical Chain': check_canonical_chain(url,response),
                'Blocked by Robots.txt': check_blocked_by_robots_txt(url),
                'Blocked by Noindex': check_blocked_by_noindex(response),
                'Blocked by Nofollow': check_blocked_by_nofollow(response),
                'Blocked by X-Robots-Tag': check_blocked_by_x_robots_tag(response),
                'Canonical HTTP to HTTPS': check_canonical_http_to_https(url, response),
                'Timed Out': check_timed_out(url),


                #### DUPLICATE CONTENT
                'No WWW Redirect': check_no_www_redirect(url),
                'Multiple Canonical Tags': check_multiple_canonical(response),
                'Duplicate Content':check_duplicate_content(response),
                'URLs with Double Slash':  check_double_slash(response),
                'No Trailing Slash':check_trailing_slash(url),
        
                #### HTTP STATUS ISSUES
      
                #'Sitemap Issues':  check_xml_sitemap_status(sitemap_url_response),
                #'Internal Links Issues': check_internal_links_status(response),
                #'External Links Issues': check_external_links_status(url, response),
                #'Hreflang Issues': check_hreflang_status(response),
                #'Images Issues': check_images_status(response),
                #'JavaScript Issues': check_javascript_status(response),
                'CSS Issues': check_css_status(response)

            }


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
    )
