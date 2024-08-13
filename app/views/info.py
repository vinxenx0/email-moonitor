# Definiciones de herramientas
tool_info = {
    'nmap': {
        'definition': "Nmap es una herramienta de escaneo de redes que permite detectar hosts y servicios en una red. En SEO, se utiliza para auditar la seguridad del sitio web, identificando vulnerabilidades que podrían ser explotadas y afectar la confianza y ranking del sitio.",
        'slogan': "Explora y asegura tu red para un SEO sólido",
        'keywords': "network, scan, security",
        'info_popup': "Nmap, abreviatura de Network Mapper, es una herramienta de código abierto utilizada para el escaneo de redes y auditoría de seguridad. Permite descubrir dispositivos activos en una red, identificar los servicios que están ejecutando, y detectar posibles vulnerabilidades. En el ámbito del SEO, la seguridad del sitio web es fundamental, ya que las brechas de seguridad pueden llevar a penalizaciones de los motores de búsqueda y a la pérdida de confianza de los usuarios. Por ejemplo, Nmap puede identificar puertos abiertos y servicios vulnerables que podrían ser puntos de entrada para ataques, permitiendo a los administradores de sitios web tomar medidas correctivas para fortalecer la seguridad y, en consecuencia, mantener o mejorar su posicionamiento en los motores de búsqueda."
    },
    'traceroute': {
        'definition': "Traceroute es una herramienta que rastrea la ruta y mide los retrasos de paquetes de datos desde un host a otro. En SEO, es vital para identificar cuellos de botella y problemas de latencia que pueden afectar la velocidad de un sitio web.",
        'slogan': "Trace the route of your packets.",
        'keywords': "Rastreando la ruta hacia un rendimiento óptimo",
        'info_popup': "Traceroute es una utilidad de diagnóstico de red que rastrea la ruta que siguen los paquetes de datos para llegar a un destino. Proporciona información sobre cada salto en la ruta, incluyendo tiempos de respuesta y posibles puntos de congestión. En el contexto de SEO, la velocidad de un sitio web es un factor crucial para la clasificación en los motores de búsqueda. Utilizando Traceroute, los profesionales de SEO pueden identificar y resolver problemas de latencia en la red que puedan estar ralentizando el tiempo de carga de un sitio web. Por ejemplo, si Traceroute muestra que hay un retraso significativo en uno de los saltos, se puede trabajar con los proveedores de servicios para optimizar esa ruta."
    },
    'aaaa': {
        'definition': "AAAA Lookup se utiliza para resolver direcciones IPv6 de un dominio. Es relevante en SEO para asegurar que un sitio web esté accesible en la moderna infraestructura de internet, mejorando la cobertura y accesibilidad global.",
        'slogan': "Preparando tu sitio para la próxima generación de Internet",
        'keywords': "dns, ipv6, lookup",
        'info_popup': "El registro AAAA (Quad-A) en DNS se utiliza para mapear un nombre de dominio a una dirección IPv6, la versión más reciente del protocolo de Internet. AAAA Lookup permite obtener estas direcciones IPv6, lo cual es cada vez más importante debido al crecimiento del uso de dispositivos conectados y la expansión de la infraestructura de internet. En términos de SEO, asegurar que un sitio web esté accesible a través de IPv6 puede mejorar la accesibilidad y rendimiento del sitio, especialmente en regiones donde IPv6 es más prevalente. Además, tener soporte para IPv6 puede ser un factor diferenciador frente a la competencia, mostrando un compromiso con la modernización y la futura prueba de la infraestructura web."
    },
    'ip': {
        'definition': "IP Lookup permite obtener información detallada sobre una dirección IP, incluyendo su ubicación geográfica y el ISP. En SEO, es esencial para analizar la distribución de tráfico y diagnosticar problemas de rendimiento de red.",
        'slogan': "Descubre todo sobre cualquier IP",
        'keywords': "ip, lookup, information",
        'info_popup': "IP Lookup es una herramienta que proporciona información detallada sobre una dirección IP específica, como su ubicación geográfica, el proveedor de servicios de Internet (ISP) y el nombre de host asociado. Esta información es útil en SEO para diversas tareas, como analizar la procedencia del tráfico web, identificar patrones sospechosos o fraudulentos, y diagnosticar problemas de red que puedan afectar la velocidad de carga de un sitio web. Por ejemplo, si una gran cantidad de tráfico proviene de una región inesperada, esto puede indicar la necesidad de ajustar la estrategia de marketing regional o investigar posibles ataques de spam."
    },
    'cname': {
        'definition': "CNAME (Canonical Name) es un tipo de registro DNS que permite mapear un dominio a otro. En SEO, es crucial para gestionar dominios y subdominios, facilitando la redirección y la gestión de URLs canónicas.",
        'slogan': "Alias perfectos para una gestión de dominios impecable",
        'keywords': "dns, cname, lookup",
        'info_popup': "El registro CNAME se utiliza en el sistema de nombres de dominio (DNS) para alias de un dominio a otro, conocido como el dominio canónico. Esto es útil para redireccionar tráfico de una URL a otra sin alterar la URL visible en el navegador del usuario. Por ejemplo, puedes tener www.ejemplo.com apuntando a ejemplo.com. En términos de SEO, los CNAMEs son útiles para gestionar subdominios, redirecciones y evitar problemas de contenido duplicado. Además, facilitan la implementación de servicios externos como plataformas de marketing o análisis que requieren redirección de subdominios."
    },
    'reverse': {
        'definition': "El Reverse Domain es una técnica que permite identificar todos los dominios asociados a una dirección IP específica. Es útil en SEO para descubrir redes de sitios web, entender la estructura de enlaces y evaluar posibles riesgos de spam.",
        'slogan': "Descubre el entramado de sitios web en una IP.",
        'keywords': "dns, reverse, lookup",
        'info_popup': "El Reverse Domain Lookup, o búsqueda inversa de dominio, permite obtener una lista de todos los dominios que comparten una misma dirección IP. Esta técnica es útil para analizar la red de sitios web de un competidor o cliente. Por ejemplo, si varios sitios comparten una misma IP, podrían estar vinculados de alguna manera, lo que puede afectar sus estrategias de SEO debido a la posible percepción de prácticas de black hat SEO. Además, esta herramienta puede ayudar a identificar si un servidor está sobrecargado con demasiados sitios, lo cual podría afectar el rendimiento y, por ende, la clasificación en los motores de búsqueda."
    },
    'whois': {
        'definition': "WHOIS es una herramienta esencial en SEO para obtener información sobre el propietario de un dominio, la fecha de registro y otros datos cruciales. Esta información ayuda a los profesionales de marketing digital a analizar la legitimidad y antigüedad de un dominio, factores que influyen en la estrategia SEO.",
        'slogan': "Descubre quién está detrás del dominio",
        'keywords': "domain, whois, registration",
        'info_popup': "WHOIS es un protocolo que se utiliza para consultar bases de datos que almacenan la información de registro de nombres de dominio en internet. Esta herramienta revela detalles importantes como el registrante, la fecha de creación y vencimiento del dominio, y los servidores DNS asociados. Por ejemplo, conocer la antigüedad de un dominio puede indicar su autoridad y confiabilidad, factores importantes en la evaluación de un sitio web para SEO. Además, WHOIS permite identificar cambios recientes en la propiedad de un dominio, lo cual puede ser relevante para entender fluctuaciones en su rendimiento SEO."
    },
    #
    'nsec3param': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'mtasts': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'arin': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'nsec': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'rrsig': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'asn': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'ipseckey': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'loc': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'ssl': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'soa': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'txt': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'bimi': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'dns': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'http': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'https': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'dnskey': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'cert': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'srv': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'dkim': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'dns_server': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'spf': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'dmarc': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'mx': {
        'definition': "",
        'slogan': "",
        'keywords': "",
        'info_popup': ""
    },
    'titles': {
        'definition': "Los títulos son esenciales para el SEO, ya que indican a los motores de búsqueda y a los usuarios de qué trata una página. Un título optimizado debe ser relevante, incluir palabras clave y atraer clics.",
        'slogan': "Títulos impactantes, clics garantizados",
        'keywords': "",
        'info_popup': "Los títulos (o title tags) son elementos HTML que especifican el título de una página web. Este título aparece en la pestaña del navegador y en los resultados de búsqueda. Un título bien escrito es crucial para el SEO porque proporciona a los motores de búsqueda información sobre el contenido de la página y ayuda a los usuarios a decidir si hacer clic en el enlace. Por ejemplo, un título como 'Guía Completa de SEO para Principiantes' es más efectivo que 'SEO'. El primero es específico, incluye palabras clave relevantes y es más probable que atraiga a usuarios interesados en aprender sobre SEO. Además, los títulos deben ser concisos, preferiblemente de menos de 60 caracteres, para evitar que se corten en los resultados de búsqueda."
    }

}