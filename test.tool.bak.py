from urllib.parse import urlencode, urlparse
import requests
import json
from bs4 import BeautifulSoup
import spider_tools

def get_page_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        #############   CANONICAL   ##############
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

        ########### SEGURIDAD ######################
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

        ############## URL ####################
        # Non ASCII Characters
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

        ############## TITULO ###############3
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

        ############# KEYWORDS #######################
        keywords_missing = not soup.find('meta', attrs={'name': 'keywords'}) if soup else True
        all_keywords = [keywords.get('content', '').strip() for keywords in soup.find_all('meta', attrs={'name': 'keywords'})] if soup else []
        keywords_duplicate = len(all_keywords) != len(set(all_keywords))
        keywords_multiple = len(soup.find_all('meta', attrs={'name': 'keywords'})) > 1 if soup else False



        page_info = {
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

            'Canonical Info': spider_tools.get_canonical_info(soup,url,response),
            'Security Info' : {
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
            },
            'Common URL Issues' : {
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
            },
            'Page Title Issues' : {
                'Missing': title_missing,
                'Duplicate': title_duplicate,
                'Over 60 characters': title_over_60_characters,
                'Below 30 characters': title_below_30_characters,
                'Same as h1': title_same_as_h1,
                'Multiple': title_multiple,
                'Outside <head>': title_outside_head
            },
            'Meta Description Issues' : {
                'Missing': meta_description_missing,
                'Duplicate': meta_description_duplicate,
                'Over 155 characters': meta_description_over_155_characters,
                'Below 70 characters': meta_description_below_70_characters,
                'Multiple': meta_description_multiple,
                'Outside <head>': meta_description_outside_head
             },
            'Meta Keywords Issues' : {
                'Missing': keywords_missing,
                'Duplicate': keywords_duplicate,
                'Multiple': keywords_multiple
           }
        }


        ############### OTHERS ############################3
        
                        # 'Indexability': check_indexability(url),
            # 'Indexability Status': indexability_status(url),
            # 'Title 1 Pixel Width': calculate_pixel_width(soup.find('title').text) if soup.find('title') else 0,
            # 'Meta Description Pixel Width': calculate_pixel_width(soup.find('meta', attrs={'name': 'description'}).get('content')) if soup.find('meta', attrs={'name': 'description'}) else 0,
            # 'Redirect URI': redirected_uri(url),
            # 'Redirect Type': redirect_type(url),
                        # 'URL Encoded Address': url_encode(url),
            # 'Redirect URL': redirected_url(url),
            # 'Redirect Type': redirect_type(url),
            # 'HTTP Version': http_version(url),
                    # 'Hash': calculate_hash(response.content),
                    # 'Text Ratio': calculate_text_ratio(response.content, soup.text),
        # 'Crawl Depth': crawl_depth(url),
        #  'Sitemap hreflang 1': sitemap_hreflang(url),
        #    'Sitemap hreflang 1 URL': sitemap_hreflang_url(url),


        return page_info

    except Exception as e:
        return {'error': str(e)}


url="https://CINEBLOG.NET"
page_info = get_page_info(url)
print(json.dumps(page_info, indent=4))