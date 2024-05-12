import re
import subprocess
from urllib.parse import urlparse
import requests
import json
from bs4 import BeautifulSoup
import app.controllers.mobile_tools

import aspell
import langid

def get_soup(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content, 'html.parser')
        else:
            return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None


def get_header_info(url):
    try:
        response = requests.head(url, allow_redirects=True)
        header_info = {
            'Header Name': [],
            'Header Value': []
        }

        for header_name, header_value in response.headers.items():
            header_info['Header Name'].append(header_name)
            header_info['Header Value'].append(header_value)

        return header_info

    except requests.RequestException as e:
        print(f"Error fetching headers for URL {url}: {e}")
        return None

def ejecutar_pa11y(url):
    command = f"pa11y -T 1 --ignore issue-code-2 --ignore issue-code-1 -r json {url} 2>/dev/null"
    process = subprocess.run(command,
                              shell=True,
                              check=False,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
    #print(process.stdout)
    return process.stdout


def analizar_ortografia(content, language='es'):
    # Configurar el corrector ortográfico
    speller = aspell.Speller('lang', language)
    
    # Tokenizar el contenido para analizar palabra por palabra
    words = content.split()
    
    # Buscar errores ortográficos y gramaticales
    spelling_errors = []
    grammar_errors = []
    for word in words:
        if not speller.check(word):
            # Si la palabra no está en el diccionario, es un error ortográfico
            spelling_errors.append(word)
            suggestions = speller.suggest(word)
            # Si hay sugerencias disponibles, consideramos que es un error gramatical
            if suggestions:
                grammar_errors.append((word, suggestions))
    
    return spelling_errors, grammar_errors

def audit_image_details(url, soup):
    images = soup.find_all('img')
    image_details = []

    for img in images:
        image_src = img.get('src', '')
        alt_text = img.get('alt', '')
        width = img.get('width', '')
        height = img.get('height', '')

        # Check if alt text is missing
        if not alt_text:
            missing_alt_text = True
        else:
            missing_alt_text = False

        # Check if alt attribute is missing
        if 'alt' not in img.attrs:
            missing_alt_attribute = True
        else:
            missing_alt_attribute = False

        # Check if alt text exceeds 100 characters
        if len(alt_text) > 100:
            alt_text_over_100_characters = True
        else:
            alt_text_over_100_characters = False

        image_details.append({
            'Image Source': image_src,
            'Alt Text': alt_text,
            'Width': width,
            'Height': height,
            'Missing Alt Text': missing_alt_text,
            'Missing Alt Attribute': missing_alt_attribute,
            'Alt Text Over 100 Characters': alt_text_over_100_characters
        })

    return {
        'URL': url,
        'Images': image_details
    }

def get_canonical_info(soup, url, response):
    canonical_link = soup.find('link', attrs={'rel': 'canonical'})
    canonical_url = canonical_link.get('href') if canonical_link else ''
    canonical_in_head = canonical_link is not None
    canonical_self_referencing = canonical_url == url
    canonicalised = canonical_url != url and canonical_url != ''
    canonical_absolute = bool(urlparse(canonical_url).netloc) if canonical_url else False
    canonical_relative = not canonical_absolute
    canonical_http_header = response.headers.get('Canonical')
    canonical_http_present = canonical_http_header is not None
    canonical_http_absolute = bool(urlparse(canonical_http_header).netloc) if canonical_http_header else False
    canonical_http_relative = not canonical_http_absolute if canonical_http_header else False
    canonical_multiple = bool(soup.find_all('link', attrs={'rel': 'canonical'})) or (canonical_http_header and canonical_http_header != canonical_url)
    canonical_multiple_conflicting = canonical_multiple and len(set(canonical_url for canonical_url in soup.find_all('link', attrs={'rel': 'canonical'}))) > 1
    canonical_non_indexable = False  # Aquí necesitarías implementar la lógica para verificar si el canonical URL es indexable o no.
    canonical_is_relative = canonical_link and not canonical_absolute
    canonical_unlinked = False  # Aquí necesitarías implementar la lógica para verificar si el canonical URL no está enlazado en el sitio web.
    canonical_outside_head = False  # Aquí necesitarías implementar la lógica para verificar si el canonical link está fuera del elemento head.

    return {
        'Contains Canonical': canonical_link is not None,
        'Self Referencing': canonical_self_referencing,
        'Canonicalised': canonicalised,
        'Canonical Absolute': canonical_absolute,
        'Canonical Relative': canonical_relative,
        'Canonical HTTP Present': canonical_http_present,
        'Canonical HTTP Absolute': canonical_http_absolute,
        'Canonical HTTP Relative': canonical_http_relative,
        'Canonical Multiple': canonical_multiple,
        'Canonical Multiple Conflicting': canonical_multiple_conflicting,
        'Canonical Non-Indexable': canonical_non_indexable,
        'Canonical Is Relative': canonical_is_relative,
        'Canonical Unlinked': canonical_unlinked,
        'Canonical Outside Head': canonical_outside_head
    }

def get_security_info(url, response, soup):
    http_url = url.startswith('http://') if url else False
    https_url = url.startswith('https://') if url else False
    mixed_content = bool(soup.find_all(lambda tag: tag.name in ['img', 'script', 'link'] and tag.get('src') and tag['src'].startswith('http://'))) if soup else False
    form_url_insecure = bool(soup.find('form', attrs={'action': lambda x: x and x.startswith('http://')})) if soup else False
    form_on_http_url = bool(soup.find('form', attrs={'action': lambda x: x and x.startswith('http://')})) if soup else False
    unsafe_cross_origin_links = bool(soup.find_all(lambda tag: tag.name == 'a' and tag.get('target') == '_blank' and ('rel' not in tag.attrs or 'noopener' not in tag.get('rel', [])))) if soup else False
    protocol_relative_resource_links = bool(soup.find_all(lambda tag: tag.name in ['img', 'script', 'link'] and tag.get('src') and tag['src'].startswith('//'))) if soup else False
    missing_hsts_header = 'strict-transport-security' not in response.headers if response else False
    missing_content_security_policy_header = 'content-security-policy' not in response.headers if response else False
    missing_x_content_type_options_header = 'x-content-type-options' not in response.headers or response.headers['x-content-type-options'] != 'nosniff' if response else False
    missing_x_frame_options_header = 'x-frame-options' not in response.headers if response else False
    missing_secure_referrer_policy_header = 'referrer-policy' not in response.headers or response.headers['referrer-policy'] not in ['no-referrer-when-downgrade', 'strict-origin-when-cross-origin', 'no-referrer', 'strict-origin'] if response else False
    bad_content_type = response.headers.get('content-type', '').split(';')[0] != 'text/html' if response else False
    
    return {
        'HTTP URLs': http_url,
        'HTTPS URLs': https_url,
        'Mixed Content': mixed_content,
        'Form URL Insecure': form_url_insecure,
        'Form on HTTP URL': form_on_http_url,
        'Unsafe Cross-Origin Links': unsafe_cross_origin_links,
        'Protocol-Relative Resource Links': protocol_relative_resource_links,
        'Missing HSTS Header': missing_hsts_header,
        'Missing Content-Security-Policy Header': missing_content_security_policy_header,
        'Missing X-Content-Type-Options Header': missing_x_content_type_options_header,
        'Missing X-Frame-Options Header': missing_x_frame_options_header,
        'Missing Secure Referrer-Policy Header': missing_secure_referrer_policy_header,
        'Bad Content Type': bad_content_type
    }

def get_common_url_issues(url):
    non_ascii_characters = any(ord(char) > 127 for char in url) if url else False
    underscores = '_' in url if url else False
    uppercase = any(char.isupper() for char in url) if url else False
    multiple_slashes = '//' in url if url else False
    repetitive_path = any(url.count(part) > 1 for part in url.split('/')) if url else False
    contains_space = ' ' in url if url else False
    internal_search = '/search' in url or '/search?' in url if url else False
    parameters = '?' in url or '&' in url if url else False
    broken_bookmark = '#' in url if url else False
    ga_tracking_parameters = any(param in url for param in ['utm=', '_ga=', '_gl=']) if url else False
    over_115_characters = len(url) > 115 if url else False
    
    return {
        'Non ASCII Characters': non_ascii_characters,
        'Underscores': underscores,
        'Uppercase': uppercase,
        'Multiple Slashes': multiple_slashes,
        'Repetitive Path': repetitive_path,
        'Contains A Space': contains_space,
        'Internal Search': internal_search,
        'Parameters': parameters,
        'Broken Bookmark': broken_bookmark,
        'GA Tracking Parameters': ga_tracking_parameters,
        'Over 115 characters': over_115_characters
    }

def get_page_title_issues(soup):

    title_missing = not soup.find('title') or not soup.find('title').text.strip() if soup else False
    all_titles = [title.text.strip() for title in soup.find_all('title')] if soup else []
    title_duplicate = len(all_titles) != len(set(all_titles))
    title_over_60_characters = any(len(title.text.strip()) > 60 for title in soup.find_all('title')) if soup else False
    title_below_30_characters = any(len(title.text.strip()) < 30 for title in soup.find_all('title')) if soup else False
    # Over X Pixels
    # Esta lógica requeriría conocer la longitud en píxeles de los títulos en la página, que normalmente se determina mediante CSS o inspección manual de la página.
    # Below X Pixels
    # Similar a "Over X Pixels", necesitaríamos información específica sobre la longitud en píxeles de los títulos en la página.
    title_same_as_h1 = any(title.text.strip() == (soup.find('h1').text.strip() if soup.find('h1') else '') for title in soup.find_all('title')) if soup else False
    title_multiple = len(soup.find_all('title')) > 1 if soup else False
    title_outside_head = any(title.find_parent('head') is None for title in soup.find_all('title')) if soup else False

    return {
                'Missing': title_missing,
                'Duplicate': title_duplicate,
                'Over 60 characters': title_over_60_characters,
                'Below 30 characters': title_below_30_characters,
                'Same as h1': title_same_as_h1,
                'Multiple': title_multiple,
                'Outside <head>': title_outside_head
            }

def get_meta_description_issues(soup):
    ########### META DESCRIPTION #########################
    meta_description_missing = not soup.find('meta', attrs={'name': 'description'}) or not soup.find('meta', attrs={'name': 'description'}).get('content').strip() if soup else False
    all_meta_descriptions = [meta.get('content').strip() for meta in soup.find_all('meta', attrs={'name': 'description'})] if soup else []
    meta_description_duplicate = len(all_meta_descriptions) != len(set(all_meta_descriptions))
    meta_description_over_155_characters = any(len(meta.get('content').strip()) > 155 for meta in soup.find_all('meta', attrs={'name': 'description'})) if soup else False
    meta_description_below_70_characters = any(len(meta.get('content').strip()) < 70 for meta in soup.find_all('meta', attrs={'name': 'description'})) if soup else False
    # Over X Pixels
    # Similar to "Over X Pixels" for page title, we would need specific information about the pixel length of meta descriptions on the page.
    # Below X Pixels
    # Similar to "Below X Pixels" for page title, we would need specific information about the pixel length of meta descriptions on the page.
    meta_description_multiple = len(soup.find_all('meta', attrs={'name': 'description'})) > 1 if soup else False
    meta_description_outside_head = any(meta.find_parent('head') is None for meta in soup.find_all('meta', attrs={'name': 'description'})) if soup else False

    return {
                'Missing': meta_description_missing,
                'Duplicate': meta_description_duplicate,
                'Over 155 characters': meta_description_over_155_characters,
                'Below 70 characters': meta_description_below_70_characters,
                'Multiple': meta_description_multiple,
                'Outside <head>': meta_description_outside_head
             }

def get_meta_keywords_issues(soup):
    ############# KEYWORDS #######################
    keywords_missing = not soup.find('meta', attrs={'name': 'keywords'}) if soup else True
    all_keywords = [keywords.get('content', '').strip() for keywords in soup.find_all('meta', attrs={'name': 'keywords'})] if soup else []
    keywords_duplicate = len(all_keywords) != len(set(all_keywords))
    keywords_multiple = len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 if soup else False

    return {
                'Missing': keywords_missing,
                'Duplicate': keywords_duplicate,
                'Multiple': keywords_multiple
           }

def get_h1_issues(soup):
    h1_missing = not soup.find('h1') or not soup.find('h1').text.strip() if soup else False
    all_h1s = [h1.text.strip() for h1 in soup.find_all('h1')] if soup else []
    h1_duplicate = len(all_h1s) != len(set(all_h1s))
    h1_over_70_characters = any(len(h1.text.strip()) > 70 for h1 in soup.find_all('h1')) if soup else False
    h1_multiple = len(soup.find_all('h1')) > 1 if soup else False
    alt_text_in_h1 = bool(soup.find('h1 img[alt]')) if soup else False
    non_sequential_h1 = not soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6']) or soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])[0].name != 'h1' if soup else False
    
    return {
        'Missing': h1_missing,
        'Duplicate': h1_duplicate,
        'Over 70 characters': h1_over_70_characters,
        'Multiple': h1_multiple,
        'Alt Text in h1': alt_text_in_h1,
        'Non-sequential': non_sequential_h1
    }

def get_h2_issues(soup):
    h2_missing = not soup.find('h2') or not soup.find('h2').text.strip() if soup else False
    all_h2s = [h2.text.strip() for h2 in soup.find_all('h2')] if soup else []
    h2_duplicate = len(all_h2s) != len(set(all_h2s))
    h2_over_70_characters = any(len(h2.text.strip()) > 70 for h2 in soup.find_all('h2')) if soup else False
    h2_multiple = len(soup.find_all('h2')) > 1 if soup else False
    non_sequential_h2 = False
    h1_exists = soup.find('h1')
    if h1_exists:
        h1_position = soup.find_all(['h1', 'h2']).index(soup.find('h1'))
        h2s_after_h1 = soup.find_all(['h1', 'h2'])[h1_position + 1:]
        non_sequential_h2 = any(tag.name == 'h2' for tag in h2s_after_h1)
    
    return {
        'Missing': h2_missing,
        'Duplicate': h2_duplicate,
        'Over 70 characters': h2_over_70_characters,
        'Multiple': h2_multiple,
        'Non-sequential': non_sequential_h2
    }

def get_directive_issues(soup, response):
    # Get meta robots tag content
    meta_robots_tag = soup.find('meta', attrs={'name': 'robots'})
    meta_robots_content = meta_robots_tag.get('content') if meta_robots_tag else ''
    
    # Get X-Robots-Tag from HTTP header
    x_robots_tag = response.headers.get('X-Robots-Tag', '')

    # Extract individual directives
    directives = {
        'Index': 'index' in meta_robots_content.lower() or 'index' in x_robots_tag.lower(),
        'Noindex': 'noindex' in meta_robots_content.lower() or 'noindex' in x_robots_tag.lower(),
        'Follow': 'follow' in meta_robots_content.lower() or 'follow' in x_robots_tag.lower(),
        'Nofollow': 'nofollow' in meta_robots_content.lower() or 'nofollow' in x_robots_tag.lower(),
        'None': 'none' in meta_robots_content.lower() or 'none' in x_robots_tag.lower(),
        'NoArchive': 'noarchive' in meta_robots_content.lower() or 'noarchive' in x_robots_tag.lower(),
        'NoSnippet': 'nosnippet' in meta_robots_content.lower() or 'nosnippet' in x_robots_tag.lower(),
        'Max-Snippet': 'max-snippet' in meta_robots_content.lower() or 'max-snippet' in x_robots_tag.lower(),
        'Max-Image-Preview': 'max-image-preview' in meta_robots_content.lower() or 'max-image-preview' in x_robots_tag.lower(),
        'Max-Video-Preview': 'max-video-preview' in meta_robots_content.lower() or 'max-video-preview' in x_robots_tag.lower(),
        'NoODP': 'noodp' in meta_robots_content.lower() or 'noodp' in x_robots_tag.lower(),
        'NoYDIR': 'noydir' in meta_robots_content.lower() or 'noydir' in x_robots_tag.lower(),
        'NoImageIndex': 'noimageindex' in meta_robots_content.lower() or 'noimageindex' in x_robots_tag.lower(),
        'NoTranslate': 'notranslate' in meta_robots_content.lower() or 'notranslate' in x_robots_tag.lower(),
        'Unavailable_After': 'unavailable_after' in meta_robots_content.lower() or 'unavailable_after' in x_robots_tag.lower(),
        'Refresh': soup.find('meta', attrs={'http-equiv': 'refresh'}) is not None,
        'Outside <head>': meta_robots_tag and not meta_robots_tag.find_parent('head')
    }

    return directives

def get_hreflang_issues(soup):
    hreflang_elements = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
    
    contains_hreflang = bool(hreflang_elements)
    
    non_200_hreflang_urls = []
    unlinked_hreflang_urls = []
    missing_return_links = []
    inconsistent_language_region_return_links = []
    non_canonical_return_links = []
    noindex_return_links = []
    incorrect_language_region_codes = []
    multiple_entries = []
    missing_self_reference = []
    not_using_canonical = []
    missing_x_default = []
    missing = []
    outside_head = []
    
    for hreflang_element in hreflang_elements:
        hreflang_url = hreflang_element.get('href')
        hreflang_status_code = requests.head(hreflang_url).status_code if hreflang_url else None
        
        if hreflang_status_code and hreflang_status_code != 200:
            non_200_hreflang_urls.append(hreflang_url)
        
        if not soup.find('a', href=hreflang_url):
            unlinked_hreflang_urls.append(hreflang_url)
        
        return_hreflang_url = soup.find('link', attrs={'rel': 'alternate', 'href': hreflang_url})
        if return_hreflang_url and not return_hreflang_url.get('hreflang'):
            missing_return_links.append(hreflang_url)
        elif return_hreflang_url and return_hreflang_url.get('hreflang') != hreflang_element.get('hreflang'):
            inconsistent_language_region_return_links.append(hreflang_url)
        
        canonical_href = soup.find('link', rel='canonical').get('href') if soup.find('link', rel='canonical') else None
        if canonical_href and canonical_href != hreflang_url:
            non_canonical_return_links.append(hreflang_url)
        
        if soup.find('meta', attrs={'name': 'robots', 'content': 'noindex'}):
            noindex_return_links.append(hreflang_url)
        
        hreflang_value = hreflang_element.get('hreflang')
        if not hreflang_value or not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', hreflang_value):
            incorrect_language_region_codes.append(hreflang_url)
        
        hreflang_entries = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': hreflang_value})
        if len(hreflang_entries) > 1:
            multiple_entries.append(hreflang_url)
        
        if not return_hreflang_url:
            missing_self_reference.append(hreflang_url)
        
        if canonical_href and canonical_href != hreflang_element.get('href'):
            not_using_canonical.append(hreflang_url)
        
        if not hreflang_element.find_parent('head'):
            outside_head.append(hreflang_url)
    
    return {
        'Contains Hreflang': contains_hreflang,
        'Non-200 Hreflang URLs': non_200_hreflang_urls,
        'Unlinked Hreflang URLs': unlinked_hreflang_urls,
        'Missing Return Links': missing_return_links,
        'Inconsistent Language & Region Return Links': inconsistent_language_region_return_links,
        'Non-Canonical Return Links': non_canonical_return_links,
        'Noindex Return Links': noindex_return_links,
        'Incorrect Language & Region Codes': incorrect_language_region_codes,
        'Multiple Entries': multiple_entries,
        'Missing Self Reference': missing_self_reference,
        'Not Using Canonical': not_using_canonical,
        'Missing X-Default': missing_x_default,
        'Missing': missing,
        'Outside <head>': outside_head
    }

def get_structured_data_issues(soup):
    structured_data = soup.find_all('script', type='application/ld+json')
    
    contains_structured_data = bool(structured_data)
    missing_structured_data = not contains_structured_data
    
    validation_errors = []
    validation_warnings = []
    parse_errors = []
    microdata_urls = []
    json_ld_urls = []
    rdfa_urls = []
    
    for script in structured_data:
        data = script.string.strip()
        
        try:
            structured_data_json = json.loads(data)
        except json.JSONDecodeError:
            parse_errors.append(data)  # Almacenamos el contenido del script en lugar del objeto Tag
            continue
        
        if '@type' in structured_data_json:
            type_value = structured_data_json.get('@type')
            if type_value == 'BreadcrumbList':
                continue  # Ignoramos el tipo de datos estructurados de migas de pan para la validación
                
            if type_value:
                if 'error' in type_value:
                    validation_errors.append(data)  # Almacenamos el contenido del script
                else:
                    validation_warnings.append(data)  # Almacenamos el contenido del script
        
        if 'Microdata' in data:
            microdata_urls.append(data)  # Almacenamos el contenido del script
        elif 'application/ld+json' in script.get('type'):
            json_ld_urls.append(data)  # Almacenamos el contenido del script
        elif 'RDFa' in data:
            rdfa_urls.append(data)  # Almacenamos el contenido del script
    
    return {
        'Contains Structured Data': contains_structured_data,
        'Missing Structured Data': missing_structured_data,
        'Validation Errors': validation_errors,
        'Validation Warnings': validation_warnings,
        'Parse Errors': parse_errors,
        'Microdata URLs': microdata_urls,
        'JSON-LD URLs': json_ld_urls,
        'RDFa URLs': rdfa_urls
    }

def get_url_details(url, soup):
    status_code = None
    status = None
    content_type = None
    size = None
    
    inlinks = len(soup.find_all('a', href=url))
    outlinks = len(soup.find_all('a'))
    
    try:
        response = requests.head(url)
        status_code = response.status_code
        status = response.reason
        content_type = response.headers.get('Content-Type')
        size = int(response.headers.get('Content-Length', 0))
    except Exception as e:
        pass
    
    return {
        'URL': url,
        'Status Code': status_code,
        'Status': status,
        'Content': content_type,
        'Size': size,
        'Inlinks': inlinks,
        'Outlinks': outlinks
    }

def validate_html(html_content):
    if isinstance(html_content, bytes):
        html_content = html_content.decode('utf-8')

    soup = BeautifulSoup(html_content, 'html.parser')

    invalid_head_elements = len(soup.find_all(lambda tag: tag.name == 'head' and tag.parent.name != 'html'))
    body_preceding_html = len(soup.find_all(lambda tag: tag.name == 'body' and tag.parent.name != 'html'))
    head_not_first = len(soup.find_all(lambda tag: tag.name == 'head' and tag.parent.contents[0].name != 'html'))
    missing_head_tag = 1 if not soup.find('head') else 0
    multiple_head_tags = len(soup.find_all('head')) - 1 if len(soup.find_all('head')) > 1 else 0
    missing_body_tag = 1 if not soup.find('body') else 0
    multiple_body_tags = len(soup.find_all('body')) - 1 if len(soup.find_all('body')) > 1 else 0

    html_size = len(html_content.encode('utf-8'))
    html_size_mb = html_size / (1024 * 1024)  # Convert bytes to megabytes

    html_over_15mb = 1 if html_size_mb > 15 else 0

    return {
        'Invalid HTML Elements In <head>': invalid_head_elements,
        'Body Element Preceding <html>': body_preceding_html,
        'Head Not First In <html> Element': head_not_first,
        'Missing <head> Tag': missing_head_tag,
        'Multiple <head> Tags': multiple_head_tags,
        'Missing <body> Tag': missing_body_tag,
        'Multiple <body> Tags': multiple_body_tags,
        'HTML Document Over 15MB': html_over_15mb
    }

## no se usa
def get_url_details(url_info):

    url_info = {
                #'Address': url,
                #'Content': response.headers.get('Content-Type', ''),
                #'Status Code': response.status_code,
                #'Status': response.reason,
                #'Size': len(response.content)
            }
    url_details = {
        'Address': url_info.get('url'),
        'Content': url_info.get('Content', ''),
        'Status Code': url_info.get('Status Code', ''),
        'Status': url_info.get('Status', ''),
        'Indexability': url_info.get('Indexability', ''),
        'Indexability Status': url_info.get('Indexability Status', ''),
        'Title 1': url_info.get('Title 1', ''),
        'Title 1 Length': url_info.get('Title 1 Length', 0),
        'Title 1 Pixel Width': url_info.get('Title 1 Pixel Width', 0),
        'Meta Description 1': url_info.get('Meta Description 1', ''),
        'Meta Description Length 1': url_info.get('Meta Description Length 1', 0),
        'Meta Description Pixel Width': url_info.get('Meta Description Pixel Width', 0),
        'Meta Keyword 1': url_info.get('Meta Keyword 1', ''),
        'Meta Keywords Length': url_info.get('Meta Keywords Length', 0),
        'h1 - 1': url_info.get('h1 - 1', ''),
        'h1 - Len-1': url_info.get('h1 - Len-1', 0),
        'h2 - 1': url_info.get('h2 - 1', ''),
        'h2 - Len-1': url_info.get('h2 - Len-1', 0),
        'Meta Robots 1': url_info.get('Meta Robots 1', ''),
        'X-Robots-Tag 1': url_info.get('X-Robots-Tag 1', ''),
        'Meta Refresh 1': url_info.get('Meta Refresh 1', ''),
        'Canonical Link Element': url_info.get('Canonical Link Element', ''),
        'rel="next" 1': url_info.get('rel="next" 1', ''),
        'rel="prev" 1': url_info.get('rel="prev" 1', ''),
        'HTTP rel="next" 1': url_info.get('HTTP rel="next" 1', ''),
        'HTTP rel="prev" 1': url_info.get('HTTP rel="prev" 1', ''),
        'Size': url_info.get('Size', 0),
        'Transferred': url_info.get('Transferred', 0),
        'Word Count': url_info.get('Word Count', 0),
        'Text Ratio': url_info.get('Text Ratio', 0),
        'Crawl Depth': url_info.get('Crawl Depth', 0),
        'Folder Depth': url_info.get('Folder Depth', 0),
        'Link Score': url_info.get('Link Score', 0),
        'Inlinks': url_info.get('Inlinks', 0),
        'Unique Inlinks': url_info.get('Unique Inlinks', 0),
        'Unique JS Inlinks': url_info.get('Unique JS Inlinks', 0),
        '% of Total': url_info.get('% of Total', 0),
        'Outlinks': url_info.get('Outlinks', 0),
        'Unique Outlinks': url_info.get('Unique Outlinks', 0),
        'Unique JS Outlinks': url_info.get('Unique JS Outlinks', 0),
        'External Outlinks': url_info.get('External Outlinks', 0),
        'Unique External Outlinks': url_info.get('Unique External Outlinks', 0),
        'Unique External JS Outlinks': url_info.get('Unique External JS Outlinks', 0),
        'Closest Similarity Match': url_info.get('Closest Similarity Match', ''),
        'No. Near Duplicates': url_info.get('No. Near Duplicates', 0),
        'Spelling Errors': url_info.get('Spelling Errors', 0),
        'Grammar Errors': url_info.get('Grammar Errors', 0),
        'Language': url_info.get('Language', ''),
        'Hash': url_info.get('Hash', ''),
        'Response Time': url_info.get('Response Time', ''),
        'Last-Modified': url_info.get('Last-Modified', ''),
        'Redirect URI': url_info.get('Redirect URI', ''),
        'Redirect Type': url_info.get('Redirect Type', ''),
        'HTTP Version': url_info.get('HTTP Version', ''),
        'URL Encoded Address': url_info.get('URL Encoded Address', ''),
        'Title 2': url_info.get('Title 2', ''),
        'Meta Description 2': url_info.get('Meta Description 2', ''),
        'h1-2': url_info.get('h1-2', ''),
        'h2-2': url_info.get('h2-2', '')
    }

    return url_details

def get_page_info(url):
    
    soup = get_soup(url)
    if soup:
        try:
            response = requests.get(url) 
            page_info = {
                
                'Canonical Info': get_canonical_info(soup, url, response),
                'Security Info': get_security_info(url, response, soup),
                'Common URL Issues': get_common_url_issues(url),
                'Page Title Issues': get_page_title_issues(soup),
                'Meta Description Issues': get_meta_description_issues(soup),
                'Meta Keywords Issues': get_meta_keywords_issues(soup),
                'H1 Issues': get_h1_issues(soup),
                'H2 Issues': get_h2_issues(soup),
                'Directives Issues': get_directive_issues(soup,response),
                'HFLang Ref Issues' : get_hreflang_issues(soup),
                'Schema ORG Issues' : get_structured_data_issues(soup),
                'Header info' : get_header_info(url),
                'Validation Issues': validate_html(response.content),
                'Mobile audit Results' : app.controllers.mobile_tools.audit_mobile_usability(url, soup),
                
                # probar velocidad con buscar en diccionario # temporal
                'Internal Details' : #get_url_details(url_info),  # Corregido aquí 
                    {
                        'Header Name': response.headers.get('Name', ''),
                        'Header Value': response.headers.get('Value', ''),
                        'URL': url,
                        'Status Code': response.status_code,
                        'Status': response.reason,
                        'Content': response.headers.get('Content-Type', ''),
                        'Size': len(response.content),
                        'Transferred': response.headers.get('Content-Length', ''),
                        'Title 1': soup.find('title').text if soup.find('title') else '',
                        'Title 1 Length': len(soup.find('title').text) if soup.find('title') else 0,
                        'h1 - 1': soup.find('h1').text if soup.find('h1') else '',
                        'h1 - Len-1': len(soup.find('h1').text) if soup.find('h1') else 0,
                        'h2 - 1': soup.find('h2').text if soup.find('h2') else '',
                        'h2 - Len-1': len(soup.find('h2').text) if soup.find('h2') else 0,
                        'Meta Description 1': soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else '',
                        'Meta Description Length 1': len(soup.find('meta', attrs={'name': 'description'}).get('content', '')) if soup.find('meta', attrs={'name': 'description'}) else 0,
                        'Meta Description Pixel Width': 0,  # Aquí necesitarías calcular la anchura en píxeles
                        'Meta Keyword 1': soup.find('meta', attrs={'name': 'keywords'}).get('content', '') if soup.find('meta', attrs={'name': 'keywords'}) else '',
                        'Meta Keywords Length': len(soup.find('meta', attrs={'name': 'keywords'}).get('content', '')) if soup.find('meta', attrs={'name': 'keywords'}) else 0,
                        'Meta Robots 1': soup.find('meta', attrs={'name': 'robots'}).get('content', '') if soup.find('meta', attrs={'name': 'robots'}) else '',
                        'X-Robots-Tag 1': response.headers.get('X-Robots-Tag', ''),
                        'Meta Refresh 1': soup.find('meta', attrs={'http-equiv': 'refresh'}).get('content', '') if soup.find('meta', attrs={'http-equiv': 'refresh'}) else '',
                        'Canonical Link Element': soup.find('link', attrs={'rel': 'canonical'}).get('href', '') if soup.find('link', attrs={'rel': 'canonical'}) else '',
                        'rel="next" 1': soup.find('link', attrs={'rel': 'next'}).get('href', '') if soup.find('link', attrs={'rel': 'next'}) else '',
                        'rel="prev" 1': soup.find('link', attrs={'rel': 'prev'}).get('href', '') if soup.find('link', attrs={'rel': 'prev'}) else '',
                        'HTTP rel="next" 1': response.headers.get('Link', '').split(';')[0].strip('<>') if response.headers.get('Link') else '',
                        'HTTP rel="prev" 1': response.headers.get('Link', '').split(';')[0].strip('<>') if response.headers.get('Link') else '',
                        'Word Count': len(soup.text.split()),
                        'Response Time': response.elapsed.total_seconds() if response.elapsed else 0,
                        'h2 Occurrences': len(soup.find_all('h2')),
                        'h2-1': soup.find('h2').text if soup.find('h2') else '',
                        'h2-1 length': len(soup.find('h2').text) if soup.find('h2') else 0,
                        'h1 Occurrences': len(soup.find_all('h1')),
                        'h1-1': soup.find('h1').text if soup.find('h1') else '',
                        'h1-1 length': len(soup.find('h1').text) if soup.find('h1') else 0,
                        'meat keywords Occurrences': len(soup.find_all('meta', attrs={'name': 'keywords'})),
                        'Meta Keyword 2': soup.find_all('meta', attrs={'name': 'keywords'})[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 else '',
                        'Meta Keyword 2 length': len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 and len(soup.find_all('meta', attrs={'name': 'keywords'}))[1].get('content', '') or 0,
                        'Description Occurrences': len(soup.find_all('meta', attrs={'name': 'description'})),
                        'Meta Description 2': soup.find_all('meta', attrs={'name': 'description'})[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'description'})) > 1 else '',
                        'Meta Description 2 length': len(soup.find_all('meta', attrs={'name': 'description'}))[1].get('content', '') if len(soup.find_all('meta', attrs={'name': 'description'})) > 1 else 0,
                        'title Occurrences': len(soup.find_all('title')),
                        'Title 2': soup.find_all('title')[1].text if len(soup.find_all('title')) > 1 else '',
                        'Title 2 length': len(soup.find_all('title')[1].text) if len(soup.find_all('title')) > 1 else 0,
                        'URL Length': len(url),
                        'Last-Modified': response.headers.get('Last-Modified', ''),
                        'Address': url,
                    },
                    
                # modulos con pestaña en menu
                'Images Issues' : audit_image_details(url,soup)
            }

            spelling_errors, grammar_errors = analizar_ortografia(response.text)
            validator = json.loads(ejecutar_pa11y(url))
                      
            return page_info, validator, spelling_errors, grammar_errors
        
        except Exception as e:
            print(f"Error processing page info: {e}")
            return {'error': str(e)}
    else:
        return {'error': 'Unable to parse HTML'}




