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
    },
    'meta-description': {
        'definition': "Las meta descriptions resumen el contenido de la página en los resultados de búsqueda, influyendo en el CTR y proporcionando una vista previa a los usuarios. Son esenciales en SEO para atraer tráfico relevante.",
        'slogan': "Tu resumen en los resultados de búsqueda",
        'keywords': "",
        'info_popup': "La meta description es una breve descripción del contenido de una página web, que aparece debajo del título en los resultados de búsqueda. Aunque no afecta directamente el ranking, una meta description bien redactada puede mejorar significativamente el CTR (Click-Through Rate), ya que ofrece a los usuarios un resumen conciso y atractivo del contenido de la página. Por ejemplo, una meta description como 'Descubre nuestra guía completa de SEO y aprende técnicas avanzadas para mejorar tu posicionamiento en Google' informa y atrae a los usuarios interesados en SEO. Las mejores prácticas incluyen mantener la longitud entre 150 y 160 caracteres, utilizar palabras clave relevantes y hacerla lo suficientemente persuasiva para incentivar a los usuarios a hacer clic en el enlace."
    },
    'meta-keywords': {
        'definition': "Las meta keywords eran utilizadas para especificar las palabras clave relevantes de una página. Aunque su uso ha disminuido en SEO moderno, entender su historia es importante para el contexto de la evolución de SEO",
        'slogan': "Del pasado del SEO, una lección de evolución",
        'keywords': "",
        'info_popup': "Las meta keywords eran una etiqueta HTML que permitía a los webmasters especificar palabras clave relacionadas con el contenido de una página web. En los primeros días de SEO, los motores de búsqueda utilizaban estas palabras clave para comprender el tema de la página y mejorar el ranking en los resultados de búsqueda. Sin embargo, con el tiempo, esta práctica fue abusada con el uso excesivo de palabras clave irrelevantes (keyword stuffing), lo que llevó a los motores de búsqueda como Google a devaluar su importancia. Hoy en día, la mayoría de los motores de búsqueda no consideran las meta keywords como un factor de ranking significativo. Sin embargo, conocer su historia ayuda a comprender cómo ha evolucionado el SEO y por qué es crucial enfocarse en la calidad del contenido y otras prácticas de optimización."
    },
    'headings': {
        'definition': "Los encabezados (headings) estructuran el contenido y mejoran la legibilidad y la SEO. Utilizados correctamente, facilitan a los motores de búsqueda y a los usuarios comprender el tema de la página.",
        'slogan': "Estructura y claridad para tu contenido",
        'keywords': "",
        'info_popup': "Los encabezados (headings) son etiquetas HTML que se utilizan para definir la estructura jerárquica del contenido de una página web, desde el H1 hasta el H6. El H1 generalmente se usa para el título principal de la página, mientras que H2 a H6 se utilizan para subtítulos y secciones dentro del contenido. Los encabezados no solo mejoran la legibilidad al dividir el texto en secciones manejables, sino que también ayudan a los motores de búsqueda a entender la estructura y el tema del contenido. Por ejemplo, en una guía sobre SEO, un H1 podría ser 'Guía Completa de SEO', mientras que los H2 podrían ser 'Qué es SEO', 'Importancia de las Palabras Clave', y así sucesivamente. La correcta utilización de encabezados con palabras clave relevantes puede mejorar el ranking y la experiencia del usuario."
    },
    'canonicals': {
        'definition': "Las etiquetas canonicals indican la versión preferida de una página duplicada, ayudando a evitar problemas de contenido duplicado. Son esenciales en SEO para consolidar señales de ranking.",
        'slogan': "Consolidando tu contenido para un mejor ranking",
        'keywords': "",
        'info_popup': "La etiqueta canonical es un elemento HTML que se utiliza para informar a los motores de búsqueda sobre la versión preferida de una página web cuando existen múltiples versiones con contenido similar o duplicado. Esto es crucial en SEO para evitar problemas de contenido duplicado que pueden diluir las señales de ranking y confundir a los motores de búsqueda. Por ejemplo, si un sitio tiene varias URLs que muestran el mismo contenido (como 'example.com/page' y 'example.com/page?ref=123'), la etiqueta canonical puede especificar cuál es la versión principal que debe indexarse, consolidando así el valor SEO de las diferentes versiones. Implementar canonicals correctamente ayuda a mantener la coherencia del contenido y a maximizar el potencial de ranking en los resultados de búsqueda."
    },
    'directives': {
        'definition': "Las directivas son instrucciones para los motores de búsqueda sobre cómo indexar y rastrear el contenido del sitio. Son vitales en SEO para controlar la visibilidad y el acceso a las páginas",
        'slogan': "Controla cómo los motores de búsqueda ven tu sitio",
        'keywords': "",
        'info_popup': "Las directivas en SEO son instrucciones específicas que se proporcionan a los motores de búsqueda sobre cómo deben rastrear e indexar el contenido de un sitio web. Estas directivas pueden incluirse en el archivo robots.txt, en las meta etiquetas del HTML, o a través de encabezados HTTP. Por ejemplo, la directiva 'noindex' puede indicarle a un motor de búsqueda que no indexe una página específica, mientras que 'nofollow' puede prevenir que los motores de búsqueda sigan ciertos enlaces. Utilizar directivas de manera adecuada permite a los webmasters controlar qué contenido es visible en los resultados de búsqueda y cómo se rastrea el sitio, optimizando así la gestión de la visibilidad y mejorando la eficiencia del rastreo. Implementar directivas correctas es esencial para evitar problemas de duplicación de contenido y gestionar adecuadamente el SEO del sitio."
    },
    'shema-org': {
        'definition': "Schema.org proporciona vocabularios para estructurar datos en páginas web, mejorando la comprensión de los motores de búsqueda y habilitando rich snippets. Es crucial en SEO para aumentar la visibilidad.",
        'slogan': "Estructura tus datos, destaca en los resultados de búsqueda",
        'keywords': "",
        'info_popup': "Schema.org es una iniciativa colaborativa que proporciona un conjunto de vocabularios para estructurar datos en páginas web, permitiendo a los motores de búsqueda comprender mejor el contenido. Mediante el uso de schema markup, los webmasters pueden definir elementos específicos como productos, eventos, reseñas, y más, que los motores de búsqueda pueden interpretar y mostrar de manera más rica en los resultados de búsqueda (rich snippets). Por ejemplo, una página de producto con schema markup puede mostrar información adicional como el precio, la disponibilidad y las calificaciones directamente en los resultados de búsqueda, lo que mejora el CTR y la visibilidad. Implementar Schema.org en el contenido web es una práctica esencial en SEO moderno para destacar en los resultados de búsqueda y proporcionar una experiencia más informativa a los usuarios."
    },
    'hreflang': {
        'definition': "Las etiquetas Hreflang indican a los motores de búsqueda la versión lingüística y regional correcta de una página, mejorando la experiencia del usuario y el SEO en sitios multilingües.",
        'slogan': "Optimiza tu contenido para una audiencia global",
        'keywords': "",
        'info_popup': "Las etiquetas Hreflang son atributos HTML utilizados para especificar la versión lingüística y regional de una página web, ayudando a los motores de búsqueda a mostrar la versión correcta a los usuarios en función de su idioma y ubicación. Esto es especialmente importante para sitios web multilingües o internacionales. Por ejemplo, un sitio web con versiones en inglés, español y francés puede usar hreflang para indicar a Google que la página example.com/en/ es para usuarios de habla inglesa,example.com/es/ es para usuarios de habla hispana, y example.com/fr/ es para usuarios de habla francesa. Implementar hreflang correctamente asegura que los usuarios sean dirigidos a la versión más relevante de la página, mejorando su experiencia y el SEO del sitio web en diferentes mercados."
    },
    'urls': {
        'definition': "Las URLs optimizadas son esenciales en SEO, ya que afectan la indexación, la visibilidad y la experiencia del usuario. Deben ser claras, concisas y contener palabras clave relevantes.",
        'slogan': "URLs claras, mejor SEO",
        'keywords': "",
        'info_popup': "Las URLs (Uniform Resource Locators) son direcciones web que indican la ubicación de un recurso en Internet. En SEO, las URLs bien estructuradas y optimizadas son cruciales porque afectan la manera en que los motores de búsqueda y los usuarios perciben y acceden al contenido de un sitio web. Una URL optimizada debe ser clara, concisa, fácil de entender y contener palabras clave relevantes. Por ejemplo, example.com/guia-seo-basica es mucho más efectiva y amigable para el SEO que example.com/page123. Las URLs claras y descriptivas no solo mejoran la experiencia del usuario, facilitando la navegación y la comprensión del contenido, sino que también ayudan a los motores de búsqueda a indexar y clasificar mejor las páginas. Implementar buenas prácticas en la creación de URLs es fundamental para el éxito en SEO."
    },
    'gzip': {
        'definition': "La compresión Gzip es una técnica para reducir el tamaño de los archivos transmitidos entre el servidor y el navegador del usuario, mejorando así el rendimiento del sitio web y la velocidad de carga. Es crucial para el SEO, ya que influye en la experiencia del usuario y en el ranking de búsqueda",
        'slogan': "Optimiza tu velocidad, mejora tu SEO con Gzip",
        'keywords': "",
        'info_popup': "Gzip es un método de compresión de datos utilizado para reducir el tamaño de los archivos HTML, CSS, JavaScript y otros recursos web transmitidos entre el servidor y el navegador del usuario. Cuando un servidor web habilita la compresión Gzip, los archivos se comprimen antes de ser enviados y se descomprimen automáticamente por el navegador del usuario, lo que resulta en tiempos de carga más rápidos y una menor cantidad de datos transferidos. Esta técnica no solo mejora significativamente la velocidad de carga de las páginas web, lo cual es un factor de ranking en SEO según Google, sino que también reduce el consumo de ancho de banda del servidor y mejora la experiencia del usuario al hacer que las páginas se carguen más rápido. Por ejemplo, si una página web tiene un archivo HTML de 1 MB y se comprime con Gzip a solo 100 KB, los usuarios experimentarán tiempos de carga mucho más rápidos sin comprometer la calidad del contenido.Implementar la compresión Gzip en un sitio web es relativamente sencillo y puede configurarse en el servidor web mediante la modificación de archivos de configuración como .htaccess en Apache o mediante la configuración de compresión en Nginx. Los beneficios de la compresión Gzip son especialmente notables en sitios web con mucho tráfico y grandes volúmenes de contenido estático, como imágenes y scripts.Para el SEO, la compresión Gzip es crucial porque Google y otros motores de búsqueda valoran la velocidad de carga rápida como un factor de ranking importante. Sitios web optimizados con Gzip no solo tienen mejor posicionamiento en los resultados de búsqueda, sino que también ofrecen una experiencia de usuario mejorada, reduciendo las tasas de rebote y aumentando el tiempo de permanencia en el sitio."
    },
    'css': {
        'definition': "Los problemas de CSS pueden afectar la apariencia y funcionalidad de un sitio web. Resolverlos es esencial para asegurar una buena experiencia de usuario y un rendimiento óptimo en SEO",
        'slogan': "Soluciona tus problemas de estilo, mejora tu SEO",
        'keywords': "",
        'info_popup': "CSS (Cascading Style Sheets) es el lenguaje utilizado para describir la presentación de un documento HTML. Los problemas de CSS, como estilos rotos o mal aplicados, pueden afectar negativamente la apariencia y la funcionalidad de un sitio web. Esto no solo perjudica la experiencia del usuario, sino que también puede impactar negativamente el SEO. Por ejemplo, un diseño desordenado o elementos mal alineados pueden aumentar la tasa de rebote y disminuir el tiempo de permanencia en el sitio. Además, los problemas de CSS pueden afectar la capacidad de los motores de búsqueda para rastrear e indexar el contenido correctamente. Identificar y resolver problemas de CSS, mediante herramientas de validación y pruebas en múltiples dispositivos, es crucial para mantener un sitio web atractivo y optimizado para los motores de búsqueda."
    },
    'deprecated-html': {
        'definition': "Las etiquetas HTML obsoletas pueden afectar la compatibilidad y el rendimiento del sitio web. Reemplazarlas es esencial para mantener estándares actuales y una buena práctica de SEO",
        'slogan': "Actualiza tu código, optimiza tu SEO",
        'keywords': "",
        'info_popup': "Las etiquetas HTML obsoletas (deprecated HTML tags) son aquellas que ya no se recomiendan en las versiones actuales de HTML y pueden ser incompatibles con los navegadores modernos. El uso de estas etiquetas puede llevar a problemas de presentación y funcionalidad en el sitio web. Por ejemplo, etiquetas como `<font>` y `<center>` han sido reemplazadas por CSS para definir estilos y alineaciones. Utilizar etiquetas HTML modernas y seguir los estándares actuales es crucial para asegurar la compatibilidad del sitio web en todos los dispositivos y navegadores. Además, mantener el código HTML actualizado y limpio ayuda a los motores de búsqueda a rastrear e indexar el contenido de manera más eficiente, mejorando así el SEO. Es importante revisar y actualizar el código regularmente para evitar el uso de etiquetas obsoletas."
    }

}