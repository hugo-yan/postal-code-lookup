#!/usr/bin/env python3
"""Generate comprehensive sitemap.xml with all country and city pages"""

import os
import glob
from datetime import datetime

# Country slug mapping
COUNTRY_SLUGS = {
    'US': 'us-postal-code',
    'CA': 'canada-postal-code',
    'GB': 'uk-postal-code',
    'DE': 'germany-postal-code',
    'FR': 'france-postal-code',
    'JP': 'japan-postal-code',
    'IN': 'india-postal-code',
    'AU': 'australia-postal-code',
    'BR': 'brazil-postal-code',
    'IT': 'italy-postal-code',
    'ES': 'spain-postal-code',
    'NL': 'netherlands-postal-code',
    'SE': 'sweden-postal-code',
    'NO': 'norway-postal-code',
    'FI': 'finland-postal-code',
    'DK': 'denmark-postal-code',
    'PL': 'poland-postal-code',
    'AT': 'austria-postal-code',
    'CH': 'switzerland-postal-code',
    'BE': 'belgium-postal-code',
    'PT': 'portugal-postal-code',
    'IE': 'ireland-postal-code',
    'NZ': 'new-zealand-postal-code',
    'ZA': 'south-africa-postal-code',
    'MX': 'mexico-postal-code',
    'RU': 'russia-postal-code',
    'TR': 'turkey-postal-code',
    'CZ': 'czech-republic-postal-code',
    'HU': 'hungary-postal-code',
    'SK': 'slovakia-postal-code',
    'HR': 'croatia-postal-code',
    'SI': 'slovenia-postal-code',
    'LT': 'lithuania-postal-code',
    'LV': 'latvia-postal-code',
    'EE': 'estonia-postal-code',
    'LU': 'luxembourg-postal-code',
    'IS': 'iceland-postal-code',
    'MT': 'malta-postal-code',
    'UK': 'united-kingdom-postal-code',
    'CN': 'china-postal-code',
    'ID': 'indonesia-postal-code',
    'GR': 'greece-postal-code',
    'SG': 'singapore-postal-code',
    'TH': 'thailand-postal-code',
    'MY': 'malaysia-postal-code',
    'PH': 'philippines-postal-code',
    'KR': 'south-korea-postal-code',
    'AE': 'uae-postal-code',
    'IL': 'israel-postal-code',
}

# Priority mapping
HIGH_PRIORITY = ['US', 'CA', 'UK', 'DE', 'FR', 'JP', 'IN', 'AU']
MEDIUM_PRIORITY = ['BR', 'IT', 'ES', 'NL', 'SE', 'NO', 'FI', 'DK', 'PL', 'AT', 'CH', 'BE', 'PT', 'IE', 'NZ', 'MX', 'RU', 'TR', 'CN', 'KR']

def get_priority(country_id):
    if country_id in HIGH_PRIORITY:
        return '0.95'
    elif country_id in MEDIUM_PRIORITY:
        return '0.9'
    else:
        return '0.85'

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = []
    
    # Homepage
    urls.append({
        'loc': 'https://postalcodelookup.info/',
        'lastmod': today,
        'changefreq': 'weekly',
        'priority': '1.0'
    })
    
    # Blog page
    urls.append({
        'loc': 'https://postalcodelookup.info/blog.html',
        'lastmod': today,
        'changefreq': 'weekly',
        'priority': '0.8'
    })
    
    # Country pages
    for country_id, slug in COUNTRY_SLUGS.items():
        if country_id == 'GB':  # Skip GB, use UK
            continue
        
        urls.append({
            'loc': f'https://postalcodelookup.info/{slug}.html',
            'lastmod': today,
            'changefreq': 'monthly',
            'priority': get_priority(country_id)
        })
    
    # City-level pages
    city_dirs = glob.glob('*-postal-code/')
    for city_dir in city_dirs:
        city_files = glob.glob(f'{city_dir}*.html')
        for city_file in city_files:
            city_name = os.path.basename(city_file).replace('-postal-code.html', '')
            city_url = city_file.replace('\\', '/')
            urls.append({
                'loc': f'https://postalcodelookup.info/{city_url}',
                'lastmod': today,
                'changefreq': 'monthly',
                'priority': '0.7'
            })
    
    # Legal pages
    legal_pages = ['privacy-policy', 'terms-of-service', 'cookie-policy', 'disclaimer']
    for page in legal_pages:
        urls.append({
            'loc': f'https://postalcodelookup.info/{page}.html',
            'lastmod': today,
            'changefreq': 'yearly',
            'priority': '0.5'
        })
    
    # Generate XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>\n'
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml)
    
    print(f"Generated sitemap.xml with {len(urls)} URLs")
    print(f"  - 1 homepage")
    print(f"  - 1 blog page")
    print(f"  - {len(COUNTRY_SLUGS) - 1} country pages")  # -1 for GB
    print(f"  - {len([u for u in urls if '/us-postal-code/' in u['loc'] or '/canada-postal-code/' in u['loc'] or '/uk-postal-code/' in u['loc']])} city pages (sample)")
    print(f"  - {len(legal_pages)} legal pages")

if __name__ == '__main__':
    main()
