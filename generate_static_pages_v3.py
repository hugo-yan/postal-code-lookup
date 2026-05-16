#!/usr/bin/env python3
"""
Generate static HTML pages for each country - V3 with advanced SEO optimization
Includes:
1. Enhanced Title and Meta Description with country keywords
2. Static page generation with SEO-friendly URLs
3. 100+ cities per country
4. Rich Schema.org markup (PostalCode, Place, ItemList, FAQPage)
5. Performance optimizations (async loading, preconnect, inline critical CSS)
6. FAQ Schema for rich snippets
7. Image SEO optimization (alt tags, dimensions)
8. City-level long-tail keyword pages
"""

import json
import re
import os

# Country name mappings for SEO-friendly URLs
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

# Display names
COUNTRY_NAMES = {
    'US': 'US',
    'CA': 'Canada',
    'GB': 'UK',
    'DE': 'Germany',
    'FR': 'France',
    'JP': 'Japan',
    'IN': 'India',
    'AU': 'Australia',
    'BR': 'Brazil',
    'IT': 'Italy',
    'ES': 'Spain',
    'NL': 'Netherlands',
    'SE': 'Sweden',
    'NO': 'Norway',
    'FI': 'Finland',
    'DK': 'Denmark',
    'PL': 'Poland',
    'AT': 'Austria',
    'CH': 'Switzerland',
    'BE': 'Belgium',
    'PT': 'Portugal',
    'IE': 'Ireland',
    'NZ': 'New Zealand',
    'ZA': 'South Africa',
    'MX': 'Mexico',
    'RU': 'Russia',
    'TR': 'Turkey',
    'CZ': 'Czech Republic',
    'HU': 'Hungary',
    'SK': 'Slovakia',
    'HR': 'Croatia',
    'SI': 'Slovenia',
    'LT': 'Lithuania',
    'LV': 'Latvia',
    'EE': 'Estonia',
    'LU': 'Luxembourg',
    'IS': 'Iceland',
    'MT': 'Malta',
    'UK': 'UK',
    'CN': 'China',
    'ID': 'Indonesia',
    'GR': 'Greece',
    'SG': 'Singapore',
    'TH': 'Thailand',
    'MY': 'Malaysia',
    'PH': 'Philippines',
    'KR': 'South Korea',
    'AE': 'UAE',
    'IL': 'Israel',
}

# SEO keywords by country
COUNTRY_KEYWORDS = {
    'US': 'US zip code lookup, US postal code finder, American zip codes, USA postcode search',
    'CA': 'Canada postal code lookup, Canadian zip codes, Canada postcode finder',
    'UK': 'UK postcode lookup, British postal codes, United Kingdom zip code',
    'DE': 'Germany postal code lookup, German zip codes, Deutschland PLZ',
    'FR': 'France postal code lookup, French zip codes, France code postal',
    'JP': 'Japan postal code lookup, Japanese zip codes, Japan yubin bangou',
    'IN': 'India postal code lookup, Indian zip codes, India PIN code',
    'AU': 'Australia postal code lookup, Australian zip codes, Aussie postcode',
    'BR': 'Brazil postal code lookup, Brazilian zip codes, Brasil CEP',
    'IT': 'Italy postal code lookup, Italian zip codes, Italia CAP',
    'ES': 'Spain postal code lookup, Spanish zip codes, Espana codigo postal',
    'NL': 'Netherlands postal code lookup, Dutch zip codes, Nederland postcode',
    'SE': 'Sweden postal code lookup, Swedish zip codes, Sverige postnummer',
    'NO': 'Norway postal code lookup, Norwegian zip codes, Norge postnummer',
    'FI': 'Finland postal code lookup, Finnish zip codes, Suomi postinumero',
    'DK': 'Denmark postal code lookup, Danish zip codes, Danmark postnummer',
    'PL': 'Poland postal code lookup, Polish zip codes, Polska kod pocztowy',
    'AT': 'Austria postal code lookup, Austrian zip codes, Osterreich PLZ',
    'CH': 'Switzerland postal code lookup, Swiss zip codes, Schweiz PLZ',
    'BE': 'Belgium postal code lookup, Belgian zip codes, Belgique code postal',
    'PT': 'Portugal postal code lookup, Portuguese zip codes, Portugal codigo postal',
    'IE': 'Ireland postal code lookup, Irish zip codes, Eircode',
    'NZ': 'New Zealand postal code lookup, NZ zip codes, Kiwi postcode',
    'ZA': 'South Africa postal code lookup, SA zip codes, RSA postcode',
    'MX': 'Mexico postal code lookup, Mexican zip codes, Mexico codigo postal',
    'RU': 'Russia postal code lookup, Russian zip codes, Rossiya indeks',
    'TR': 'Turkey postal code lookup, Turkish zip codes, Turkiye posta kodu',
    'CZ': 'Czech Republic postal code lookup, Czech zip codes, Ceska republika PSC',
    'HU': 'Hungary postal code lookup, Hungarian zip codes, Magyarorszag iranyitoszam',
    'SK': 'Slovakia postal code lookup, Slovak zip codes, Slovensko PSC',
    'HR': 'Croatia postal code lookup, Croatian zip codes, Hrvatska postanski broj',
    'SI': 'Slovenia postal code lookup, Slovenian zip codes, Slovenija postna stevilka',
    'LT': 'Lithuania postal code lookup, Lithuanian zip codes, Lietuvos pasto indeksas',
    'LV': 'Latvia postal code lookup, Latvian zip codes, Latvijas pasta indekss',
    'EE': 'Estonia postal code lookup, Estonian zip codes, Eesti postiindeks',
    'LU': 'Luxembourg postal code lookup, Luxembourgish zip codes',
    'IS': 'Iceland postal code lookup, Icelandic zip codes, Island postnumer',
    'MT': 'Malta postal code lookup, Maltese zip codes',
    'CN': 'China postal code lookup, Chinese zip codes, Zhongguo youbian',
    'ID': 'Indonesia postal code lookup, Indonesian zip codes, Kode pos Indonesia',
    'GR': 'Greece postal code lookup, Greek zip codes, Ellada taxydromikos kodikas',
    'SG': 'Singapore postal code lookup, Singaporean zip codes',
    'TH': 'Thailand postal code lookup, Thai zip codes, Prathet Thai post code',
    'MY': 'Malaysia postal code lookup, Malaysian zip codes, Poskod Malaysia',
    'PH': 'Philippines postal code lookup, Filipino zip codes, ZIP code Philippines',
    'KR': 'South Korea postal code lookup, Korean zip codes, Hanguk ujeongbeonho',
    'AE': 'UAE postal code lookup, Dubai zip codes, Emirates postcode',
    'IL': 'Israel postal code lookup, Israeli zip codes, Yisrael mikud',
}

# Flag code mapping
FLAG_CODE_MAP = {
    'UK': 'gb',
    'GB': 'gb',
}

# Default coordinates for countries
DEFAULT_COORDS = {
    'US': [39.8283, -98.5795], 'CA': [56.1304, -106.3468], 'JP': [36.2048, 138.2529],
    'FR': [46.2276, 2.2137], 'ZA': [-30.5595, 22.9375], 'UK': [55.3781, -3.4360],
    'GB': [55.3781, -3.4360], 'BR': [-14.2350, -51.9253], 'DE': [51.1657, 10.4515],
    'ID': [-0.7893, 113.9213], 'PL': [51.9194, 19.1451], 'IT': [41.8719, 12.5674],
    'MX': [23.6345, -102.5528], 'NO': [60.4720, 8.4689], 'IN': [20.5937, 78.9629],
    'NZ': [-40.9006, 174.8860], 'AU': [-25.2744, 133.7751], 'RU': [61.5240, 105.3188],
    'CN': [35.8617, 104.1954], 'TR': [38.9637, 35.2433], 'ES': [40.4637, -3.7492],
    'SE': [60.1282, 18.6435], 'LT': [55.1694, 23.8813], 'GR': [39.0742, 21.8243],
    'PR': [18.2208, -66.5901], 'TH': [15.8700, 100.9925], 'FI': [61.9241, 25.7482],
    'PT': [39.3999, -8.2245], 'BE': [50.5039, 4.4699], 'DK': [56.2639, 9.5018],
    'HR': [45.1000, 15.2000], 'NL': [52.1326, 5.2913], 'HU': [47.1625, 19.5033],
    'AT': [47.5162, 14.5501], 'CH': [46.8182, 8.2275], 'CZ': [49.8175, 15.4730],
    'SK': [48.6690, 19.6990], 'SG': [1.3521, 103.8198], 'LU': [49.8153, 6.1296],
    'IE': [53.1424, -7.6921], 'LV': [56.8796, 24.6032], 'EE': [58.5953, 25.0136],
    'SI': [46.1512, 14.9955], 'IS': [64.9631, -19.0208], 'MT': [35.9375, 14.3754],
    'MY': [4.2105, 101.9758], 'PH': [12.8797, 121.7740], 'KR': [35.9078, 127.7669],
    'AE': [23.4241, 53.8478], 'IL': [31.0461, 34.8516],
}


def parse_mock_data():
    """Parse the mockData.js file to extract full country data"""
    with open('mockData.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract country data using regex
    countries = []
    country_pattern = r'\{\s*id:\s*"([A-Z]{2})",\s*name:\s*"([^"]+)"'
    matches = re.finditer(country_pattern, content)

    for match in matches:
        country_id = match.group(1)
        country_name = match.group(2)
        countries.append({
            'id': country_id,
            'name': country_name
        })

    return countries


def extract_country_data_from_js(country_id):
    """Extract full country data from mockData.js using a robust approach"""
    with open('mockData.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the country section - look for the country ID and capture until the next country or end
    country_start = content.find(f'id: "{country_id}"')
    if country_start == -1:
        return None

    # Find the start of this country object
    obj_start = content.rfind('{', 0, country_start)

    # Find the end of this country object by tracking braces
    brace_count = 0
    obj_end = obj_start
    in_string = False
    escape_next = False

    for i in range(obj_start, len(content)):
        char = content[i]

        if escape_next:
            escape_next = False
            continue

        if char == '\\':
            escape_next = True
            continue

        if char == '"' and not escape_next:
            in_string = not in_string
            continue

        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    obj_end = i + 1
                    break

    country_text = content[obj_start:obj_end]

    # Parse states
    states_data = []

    # Find states array
    states_match = re.search(r'states:\s*\[(.*)\]\s*\}\s*$', country_text, re.DOTALL)
    if not states_match:
        return {'states': []}

    states_text = states_match.group(1)

    # Extract each state - find state objects by looking for id: "US_0" patterns
    state_start_pattern = r'\{\s*id:\s*"' + country_id + r'_\d+"'
    state_starts = list(re.finditer(state_start_pattern, states_text))

    for i, state_start_match in enumerate(state_starts):
        state_start_pos = state_start_match.start()

        # Find the end of this state object
        if i + 1 < len(state_starts):
            state_end_pos = state_starts[i + 1].start()
        else:
            # Find the last closing brace before the end of states array
            state_end_pos = len(states_text)

        state_text = states_text[state_start_pos:state_end_pos]

        # Extract state id and name
        state_id_match = re.search(r'id:\s*"([^"]+)"', state_text)
        state_name_match = re.search(r'name:\s*"([^"]+)"', state_text)

        if not state_id_match or not state_name_match:
            continue

        state_id = state_id_match.group(1)
        state_name = state_name_match.group(1)

        # Extract cities
        cities = []

        # Find city objects
        city_pattern = r'\{\s*id:\s*"' + re.escape(state_id) + r'_\d+",\s*name:\s*"([^"]+)"'
        city_matches = list(re.finditer(city_pattern, state_text))

        for j, city_match in enumerate(city_matches):
            city_name = city_match.group(1)
            city_id_match = re.search(r'id:\s*"([^"]+)"', city_match.group(0))
            city_id = city_id_match.group(1) if city_id_match else f"{state_id}_{j}"

            # Extract postal codes for this city
            postal_codes = []

            # Find the city object text
            city_start = city_match.start()
            if j + 1 < len(city_matches):
                city_end = city_matches[j + 1].start()
            else:
                city_end = len(state_text)

            city_text = state_text[city_start:city_end]

            # Extract postal codes
            pc_match = re.search(r'postalCodes:\s*\[(.*?)\]', city_text, re.DOTALL)
            if pc_match:
                pc_text = pc_match.group(1)
                code_matches = re.finditer(r'code:\s*"([^"]+)"', pc_text)
                for code_match in code_matches:
                    postal_codes.append({'code': code_match.group(1)})

            cities.append({
                'id': city_id,
                'name': city_name,
                'postalCodes': postal_codes
            })

        states_data.append({
            'id': state_id,
            'name': state_name,
            'cities': cities
        })

    return {'states': states_data}


def generate_faq_schema(display_name, country_id):
    """Generate FAQPage schema for rich snippets"""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"How do I find a postal code in {display_name}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"To find a postal code in {display_name}, simply enter the city name or address in our search box above. Select your location from the dropdown suggestions, and the postal code will be displayed along with an interactive map showing the exact location."
                }
            },
            {
                "@type": "Question",
                "name": f"How many digits are in a {display_name} postal code?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"The number of digits in a {display_name} postal code varies depending on the specific postal system. Our tool provides the correct format for each location within {display_name}."
                }
            },
            {
                "@type": "Question",
                "name": f"Can I search for postal codes by city name in {display_name}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Yes, you can search for postal codes by city name in {display_name}. Our database covers thousands of cities and towns across {display_name}. Simply type the city name in the search box and select from the autocomplete suggestions."
                }
            },
            {
                "@type": "Question",
                "name": f"Is this {display_name} postal code lookup free to use?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Yes, our {display_name} postal code lookup tool is completely free to use. You can search for unlimited postal codes across {display_name} without any registration or fees."
                }
            },
            {
                "@type": "Question",
                "name": f"How accurate is the postal code data for {display_name}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Our postal code data for {display_name} is sourced from reliable databases including GeoNames.org and OpenStreetMap. While we strive for accuracy, we recommend verifying critical postal codes with your local postal service for official purposes."
                }
            }
        ]
    }


def generate_static_page_v3(country_id, country_data):
    """Generate an optimized static HTML page for a country with V3 features"""
    slug = COUNTRY_SLUGS.get(country_id, f"{country_id.lower()}-postal-code")
    display_name = COUNTRY_NAMES.get(country_id, country_data.get('name', country_id))
    flag_code = FLAG_CODE_MAP.get(country_id, country_id.lower())
    coords = DEFAULT_COORDS.get(country_id, [0, 0])
    keywords = COUNTRY_KEYWORDS.get(country_id, f"{display_name.lower()} postal code, {display_name.lower()} zip code")

    # Get all cities for this country
    cities = []
    states = []
    for state in country_data.get('states', []):
        states.append(state['name'])
        for city in state.get('cities', []):
            cities.append({
                'id': city['id'],
                'name': city['name'],
                'state': state['name'],
                'stateId': state['id'],
                'postalCodes': city.get('postalCodes', []),
            })

    cities.sort(key=lambda x: x['name'])
    states.sort()

    # Generate city options HTML (up to 200 cities)
    city_options = '\n'.join([
        f'          <option value="{c["id"]}">{c["name"]} ({c["state"]})</option>'
        for c in cities[:200]
    ])

    # Generate state links HTML
    state_links = '\n'.join([
        f'          <a href="#{state.replace(" ", "-").lower()}" class="state-link" data-state="{state}">{state}</a>'
        for state in states[:60]
    ])

    # Generate popular cities list (first 50 for SEO)
    popular_cities = cities[:50]
    popular_cities_html = '\n'.join([
        f'        <div class="city-link-item" data-city="{c["name"]}">{c["name"]} ({c["state"]})</div>'
        for c in popular_cities
    ])

    # Generate city links for SEO (first 20 with postal codes)
    city_links_seo = []
    for c in popular_cities[:20]:
        if c['postalCodes']:
            pc = c['postalCodes'][0]['code']
            city_links_seo.append({
                'name': c['name'],
                'state': c['state'],
                'code': pc
            })

    # Generate Schema.org structured data - Rich markup
    schema_webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{display_name} Postal Code Lookup",
        "description": f"Search postal codes and zip codes for cities in {display_name}. Find postal code information by city name or address.",
        "url": f"https://postalcodelookup.info/{slug}.html",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://postalcodelookup.info/"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": f"{display_name} Postal Code Lookup",
                    "item": f"https://postalcodelookup.info/{slug}.html"
                }
            ]
        }
    }

    # PostalCode schema for top cities
    schema_postalcodes = []
    for i, c in enumerate(city_links_seo[:10]):
        schema_postalcodes.append({
            "@context": "https://schema.org",
            "@type": "PostalCode",
            "postalCode": c['code'],
            "addressLocality": c['name'],
            "addressRegion": c['state'],
            "addressCountry": display_name
        })

    # ItemList schema for cities
    schema_itemlist = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"Popular Cities in {display_name}",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": f"{c['name']} Postal Code",
                "description": f"Postal code {c['code']} for {c['name']}, {c['state']}, {display_name}"
            }
            for i, c in enumerate(city_links_seo[:15])
        ]
    }

    # Organization schema
    schema_org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Postal Code Lookup",
        "url": "https://postalcodelookup.info/",
        "logo": "https://postalcodelookup.info/favicon.ico"
    }

    # FAQ schema
    schema_faq = generate_faq_schema(display_name, country_id)

    # Combine all schemas
    all_schemas = [schema_webpage, schema_itemlist, schema_org, schema_faq] + schema_postalcodes[:5]

    # Generate FAQ HTML section
    faq_html = f'''
      <!-- FAQ Section for SEO -->
      <section class="faq-section" style="margin-top: 2rem; padding: 1.5rem; background: var(--color-surface); border-radius: var(--radius-lg);">
        <h2 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--color-text);">Frequently Asked Questions about {display_name} Postal Codes</h2>
        <div class="faq-list" style="display: flex; flex-direction: column; gap: 1rem;">
          <details class="faq-item" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
            <summary style="font-weight: 600; cursor: pointer; color: var(--color-primary);">How do I find a postal code in {display_name}?</summary>
            <p style="margin-top: 0.5rem; color: var(--color-text-muted); line-height: 1.6;">
              To find a postal code in {display_name}, simply enter the city name or address in our search box above. Select your location from the dropdown suggestions, and the postal code will be displayed along with an interactive map showing the exact location.
            </p>
          </details>
          <details class="faq-item" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
            <summary style="font-weight: 600; cursor: pointer; color: var(--color-primary);">How many digits are in a {display_name} postal code?</summary>
            <p style="margin-top: 0.5rem; color: var(--color-text-muted); line-height: 1.6;">
              The number of digits in a {display_name} postal code varies depending on the specific postal system. Our tool provides the correct format for each location within {display_name}.
            </p>
          </details>
          <details class="faq-item" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
            <summary style="font-weight: 600; cursor: pointer; color: var(--color-primary);">Can I search for postal codes by city name in {display_name}?</summary>
            <p style="margin-top: 0.5rem; color: var(--color-text-muted); line-height: 1.6;">
              Yes, you can search for postal codes by city name in {display_name}. Our database covers thousands of cities and towns across {display_name}. Simply type the city name in the search box and select from the autocomplete suggestions.
            </p>
          </details>
          <details class="faq-item" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
            <summary style="font-weight: 600; cursor: pointer; color: var(--color-primary);">Is this {display_name} postal code lookup free to use?</summary>
            <p style="margin-top: 0.5rem; color: var(--color-text-muted); line-height: 1.6;">
              Yes, our {display_name} postal code lookup tool is completely free to use. You can search for unlimited postal codes across {display_name} without any registration or fees.
            </p>
          </details>
          <details class="faq-item" style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
            <summary style="font-weight: 600; cursor: pointer; color: var(--color-primary);">How accurate is the postal code data for {display_name}?</summary>
            <p style="margin-top: 0.5rem; color: var(--color-text-muted); line-height: 1.6;">
              Our postal code data for {display_name} is sourced from reliable databases including GeoNames.org and OpenStreetMap. While we strive for accuracy, we recommend verifying critical postal codes with your local postal service for official purposes.
            </p>
          </details>
        </div>
      </section>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">

  <title>{display_name} Postal Code Lookup | Find Zip Codes in {display_name} 2026</title>
  <meta name="description" content="Free {display_name} postal code lookup tool. Search zip codes for {len(cities)}+ cities in {display_name}. Find {display_name} postal code information by city name or address with interactive map.">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="https://postalcodelookup.info/{slug}.html">
  <meta name="author" content="Postal Code Lookup">
  <meta name="geo.region" content="{country_id}">
  <meta name="geo.placename" content="{display_name}">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{display_name} Postal Code Lookup | Find Zip Codes in {display_name}">
  <meta property="og:description" content="Search postal codes for {len(cities)}+ cities in {display_name}. Free lookup tool with interactive map.">
  <meta property="og:url" content="https://postalcodelookup.info/{slug}.html">
  <meta property="og:site_name" content="Postal Code Lookup">
  <meta property="og:image" content="https://postalcodelookup.info/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{display_name} Postal Code Lookup">
  <meta name="twitter:description" content="Search postal codes for {len(cities)}+ cities in {display_name}">
  <meta name="twitter:image" content="https://postalcodelookup.info/og-image.jpg">

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%231E40AF' width='100' height='100' rx='20'/%3E%3Ctext x='50' y='68' font-size='50' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'%3EP%3C/text%3E%3C/svg%3E">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="dns-prefetch" href="https://unpkg.com">
  <link rel="dns-prefetch" href="https://nominatim.openstreetmap.org">

  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="country.css">

  <!-- Leaflet CSS for Map - Load async -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"></noscript>

  <!-- Schema.org Structured Data -->
  <script type="application/ld+json">
  {json.dumps(all_schemas, indent=2)}
  </script>
</head>

<body>
  <a href="#main-content" class="visually-hidden">Skip to main content</a>

  <header class="header" role="banner">
    <div class="header-content">
      <a href="index.html" class="logo" aria-label="Postal Code Lookup Home">
        <svg class="logo-icon-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path fill-rule="evenodd" d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z" clip-rule="evenodd" />
          <path fill-rule="evenodd" d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z" clip-rule="evenodd" />
        </svg>
        <span>Postal Code Lookup</span>
      </a>
      <nav aria-label="Main navigation">
        <a href="index.html" class="back-link">&#8592; Back to Countries</a>
      </nav>
    </div>
  </header>

  <main id="main-content" class="main-content">
    <div class="container">
      <!-- Breadcrumb Navigation -->
      <nav aria-label="Breadcrumb" class="breadcrumb">
        <ol itemscope itemtype="https://schema.org/BreadcrumbList">
          <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <a itemprop="item" href="index.html"><span itemprop="name">Home</span></a>
            <meta itemprop="position" content="1" />
          </li>
          <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
            <span itemprop="name">{display_name} Postal Code</span>
            <meta itemprop="position" content="2" />
          </li>
        </ol>
      </nav>

      <!-- Top Section: Search + About -->
      <div class="top-section">
        <!-- Left: Search Tool -->
        <section class="search-tool" aria-labelledby="search-heading">
          <div class="search-tool-header">
            <img id="search-country-flag" class="search-country-flag" src="flags/{flag_code}.png" alt="{display_name} national flag - {display_name} postal code lookup" width="24" height="18" loading="eager">
            <h1 id="search-heading" class="search-tool-title">
              {display_name} Postal Code Lookup
            </h1>
          </div>

          <div class="search-box">
            <label for="city-search" class="form-label">Enter Address / Place / Location / City in {display_name}</label>
            <div class="autocomplete-wrapper">
              <svg class="form-input-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
              </svg>
              <input
                type="search"
                id="city-search"
                class="form-input search-input"
                placeholder="Enter a location in {display_name}..."
                autocomplete="off"
                aria-autocomplete="list"
                aria-controls="suggestions-list"
                aria-label="Search for a city in {display_name}"
              >
              <ul id="suggestions-list" class="suggestions-list" role="listbox" aria-label="City suggestions"></ul>
            </div>
          </div>

          <button id="show-btn" class="show-btn" disabled>
            Show Postal Code
          </button>
        </section>

        <!-- Right: About Section -->
        <section class="about-tool" aria-labelledby="about-heading">
          <h2 id="about-heading" class="about-title">About {display_name} Postal Code Lookup</h2>
          <div class="about-content">
            <p>
              This is an online tool to search postal code of a place, address or city in <strong>{display_name}</strong>.
              Select the name of the Place/Address/City (in {display_name}) from the suggested list.
              This will display the postal code of the selected location from {display_name} on the map.
            </p>
            <p><strong>Note that the postal code may be searched with nearby approximation.</strong></p>
            <p>We cover <strong>{len(cities)} cities</strong> across <strong>{len(states)} states/provinces</strong> in {display_name}.</p>
          </div>
        </section>
      </div>

      <!-- Ad Unit: Leaderboard -->
      <div class="ad-container">
        <span class="ad-label">Advertisement</span>
      </div>

      <!-- Results Section -->
      <section id="results-section" class="results-section" aria-live="polite" style="display: none;">
        <div class="results-layout">
          <div class="postal-info">
            <h3 class="results-title">Postal Code Information</h3>
            <div id="postal-details" class="postal-details"></div>
          </div>

          <div class="map-container">
            <h3 class="results-title">Location on Map</h3>
            <div id="map" class="map"></div>
          </div>
        </div>
      </section>

      <!-- Ad Unit: Leaderboard -->
      <div class="ad-container">
        <span class="ad-label">Advertisement</span>
      </div>

      <!-- Bottom Section: Cities + States -->
      <div class="bottom-section">
        <!-- Left: Popular Cities -->
        <section class="popular-cities" aria-labelledby="cities-heading">
          <h2 id="cities-heading" class="section-title">
            Popular Cities in {display_name}
          </h2>
          <p class="cities-note">
            Below is the select list of some major cities from {display_name}. Click on the "Show Postal Code" button to go get its postal code.
          </p>

          <div class="cities-select-wrapper">
            <select id="cities-select" class="cities-select" aria-label="Select a city in {display_name}">
              <option value="">Select a city...</option>
{city_options}
            </select>
          </div>

          <button id="show-selected-btn" class="show-btn">
            Show Postal Code
          </button>

          <!-- Popular Cities Links for SEO -->
          <div class="popular-cities-links" style="margin-top: 1.5rem;">
            <h3 style="font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: 0.75rem;">Popular {display_name} Cities with Postal Codes:</h3>
            <div class="city-links-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.5rem; font-size: 0.8rem;">
{popular_cities_html}
            </div>
          </div>
        </section>

        <!-- Right: State/Province List -->
        <section class="states-list" aria-labelledby="states-heading">
          <h2 id="states-heading" class="states-title">State/Province level Postal Code Search:</h2>
          <p style="font-size: 0.8rem; color: var(--color-text-muted); margin-bottom: 1rem;">
            Click on a state/province to filter cities in that region.
          </p>
          <div id="states-container" class="states-container">
{state_links}
          </div>
        </section>
      </div>

      <!-- SEO Content Section -->
      <section class="seo-content" style="margin-top: 2rem; padding: 1.5rem; background: var(--color-surface); border-radius: var(--radius-lg);">
        <h2 style="font-size: 1.25rem; margin-bottom: 1rem; color: var(--color-text);">{display_name} Postal Code Information</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
          <div>
            <h3 style="font-size: 1rem; margin-bottom: 0.5rem; color: var(--color-primary);">About {display_name} Postal Codes</h3>
            <p style="font-size: 0.875rem; line-height: 1.6; color: var(--color-text-muted);">
              {display_name} uses a postal code system to help deliver mail efficiently. 
              Our database covers {len(cities)} cities and towns across {len(states)} states/provinces.
              Use our lookup tool to find the correct postal code for any address in {display_name}.
            </p>
          </div>
          <div>
            <h3 style="font-size: 1rem; margin-bottom: 0.5rem; color: var(--color-primary);">How to Use</h3>
            <p style="font-size: 0.875rem; line-height: 1.6; color: var(--color-text-muted);">
              1. Enter a city name or address in the search box<br>
              2. Select from the autocomplete suggestions<br>
              3. Click "Show Postal Code" to see results<br>
              4. View the location on the interactive map
            </p>
          </div>
        </div>
      </section>
{faq_html}
    </div>

    <!-- Data Accuracy Notice -->
    <div class="data-notice" role="note" aria-label="Data accuracy notice">
      <div class="data-notice-icon">&#9888;&#65039;</div>
      <div class="data-notice-content">
        <strong>Data Disclaimer:</strong> Postal code information provided is for reference only and may not reflect the most current data. For official verification, please contact your local postal service or visit the official website.
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="footer" role="contentinfo">
    <div class="footer-content">
      <nav class="footer-links" aria-label="Footer navigation">
        <a href="index.html" class="footer-link">Postal Code Home</a>
        <a href="blog.html" class="footer-link">Blog</a>
        <a href="privacy-policy.html" class="footer-link">Privacy Policy</a>
        <a href="terms-of-service.html" class="footer-link">Terms of Service</a>
        <a href="cookie-policy.html" class="footer-link">Cookie Policy</a>
        <a href="disclaimer.html" class="footer-link">Disclaimer</a>
      </nav>
      <p style="text-align: center; margin-top: var(--space-md); font-size: 0.75rem; color: rgba(255,255,255,0.5);">
        &copy; 2026 Postal Code Lookup. All rights reserved.
      </p>
      <p style="text-align: center; margin-top: var(--space-sm); font-size: 0.6875rem; color: rgba(255,255,255,0.4);">
        Data sources: <a href="https://www.geonames.org/" target="_blank" rel="noopener noreferrer" style="color: rgba(255,255,255,0.5); text-decoration: underline;">GeoNames.org</a> | <a href="https://www.openstreetmap.org/" target="_blank" rel="noopener noreferrer" style="color: rgba(255,255,255,0.5); text-decoration: underline;">OpenStreetMap</a>
      </p>
    </div>
  </footer>

  <!-- Toast Container -->
  <div id="toast-container"></div>

  <!-- Leaflet JS - Async loading for performance -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin="" async></script>

  <!-- Cookie Consent Banner -->
  <div id="cookie-consent" class="cookie-consent" style="display: none;">
    <div class="cookie-consent-content">
      <p>We use cookies to enhance your experience and serve personalized ads. By continuing to use our site, you agree to our <a href="cookie-policy.html">Cookie Policy</a>.</p>
      <div class="cookie-consent-buttons">
        <button id="cookie-accept" class="cookie-btn cookie-btn-primary">Accept All</button>
        <button id="cookie-decline" class="cookie-btn cookie-btn-secondary">Decline</button>
      </div>
    </div>
  </div>

  <script>
    // Country data embedded for static page
    window.countryId = "{country_id}";
    window.countryName = "{display_name}";
    window.countryCoords = {coords};
    window.totalCities = {len(cities)};
    window.totalStates = {len(states)};
  </script>
  <script src="mockData.js"></script>
  <script src="country.js"></script>
  <script>
    // Cookie Consent Logic
    (function() {{
      const consentBanner = document.getElementById('cookie-consent');
      const acceptBtn = document.getElementById('cookie-accept');
      const declineBtn = document.getElementById('cookie-decline');
      
      const cookieChoice = localStorage.getItem('cookieConsent');
      
      if (!cookieChoice) {{
        consentBanner.style.display = 'block';
      }}
      
      acceptBtn.addEventListener('click', function() {{
        localStorage.setItem('cookieConsent', 'accepted');
        consentBanner.style.display = 'none';
        if (typeof initAds === 'function') {{
          initAds();
        }}
      }});
      
      declineBtn.addEventListener('click', function() {{
        localStorage.setItem('cookieConsent', 'declined');
        consentBanner.style.display = 'none';
      }});
    }})();
  </script>
</body>
</html>'''

    return slug, html


def generate_city_pages(country_id, country_data, country_slug):
    """Generate city-level pages for top cities"""
    display_name = COUNTRY_NAMES.get(country_id, country_data.get('name', country_id))
    flag_code = FLAG_CODE_MAP.get(country_id, country_id.lower())
    coords = DEFAULT_COORDS.get(country_id, [0, 0])

    cities = []
    for state in country_data.get('states', []):
        for city in state.get('cities', []):
            cities.append({
                'id': city['id'],
                'name': city['name'],
                'state': state['name'],
                'postalCodes': city.get('postalCodes', []),
            })

    # Only generate pages for top 10 cities per country
    top_cities = cities[:10]
    generated = []

    for city in top_cities:
        if not city['postalCodes']:
            continue

        city_slug = city['name'].lower().replace(' ', '-').replace(',', '')
        filename = f"{country_slug}/{city_slug}-postal-code.html"

        # Create directory if needed
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        pc = city['postalCodes'][0]['code']

        # City page Schema
        schema_city = {
            "@context": "https://schema.org",
            "@type": "PostalCode",
            "postalCode": pc,
            "addressLocality": city['name'],
            "addressRegion": city['state'],
            "addressCountry": display_name
        }

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{city['name']} Postal Code {pc} | {display_name}</title>
  <meta name="description" content="Postal code for {city['name']}, {city['state']}, {display_name}. Find zip codes and address information for {city['name']}.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://postalcodelookup.info/{filename}">
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="../country.css">
  <script type="application/ld+json">
  {json.dumps(schema_city, indent=2)}
  </script>
</head>
<body>
  <header class="header" role="banner">
    <div class="header-content">
      <a href="../index.html" class="logo">Postal Code Lookup</a>
      <nav><a href="../{country_slug}.html" class="back-link">&#8592; Back to {display_name}</a></nav>
    </div>
  </header>

  <main class="main-content">
    <div class="container">
      <section class="search-tool">
        <h1>{city['name']} Postal Code</h1>
        <div class="postal-info" style="padding: 2rem; background: var(--color-surface); border-radius: var(--radius-lg); margin: 1rem 0;">
          <p><strong>City:</strong> {city['name']}</p>
          <p><strong>State/Province:</strong> {city['state']}</p>
          <p><strong>Country:</strong> {display_name}</p>
          <p><strong>Postal Code:</strong> <span style="font-size: 1.5rem; color: var(--color-primary);">{pc}</span></p>
        </div>
        <p style="margin-top: 1rem;">
          <a href="../{country_slug}.html" style="color: var(--color-primary);">Search other cities in {display_name}</a>
        </p>
      </section>
    </div>
  </main>

  <footer class="footer">
    <div class="footer-content">
      <p>&copy; 2026 Postal Code Lookup</p>
    </div>
  </footer>
</body>
</html>'''

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        generated.append({
            'city': city['name'],
            'filename': filename
        })

    return generated


def main():
    """Main function to generate all optimized static pages"""
    print("Starting optimized static page generation (V3)...")

    # Parse mock data to get country list
    countries = parse_mock_data()
    print(f"Found {len(countries)} countries in mockData.js")

    generated_pages = []
    city_pages_total = 0

    for country in countries:
        country_id = country['id']
        country_name = country['name']

        # Skip duplicates (UK/GB) and invalid IDs
        if country_id == 'GB' or len(country_id) != 2:
            continue

        # Extract full country data from JS file
        country_data = extract_country_data_from_js(country_id)
        if not country_data:
            country_data = {'name': country_name, 'states': []}

        slug, html = generate_static_page_v3(country_id, country_data)
        filename = f"{slug}.html"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        generated_pages.append({
            'id': country_id,
            'name': country_name,
            'slug': slug,
            'filename': filename,
            'cities': sum(len(s.get('cities', [])) for s in country_data.get('states', [])),
            'states': len(country_data.get('states', []))
        })
        print(f"Generated: {filename} ({country_name} - {generated_pages[-1]['cities']} cities, {generated_pages[-1]['states']} states)")

        # Generate city-level pages for top cities
        city_pages = generate_city_pages(country_id, country_data, slug)
        city_pages_total += len(city_pages)
        if city_pages:
            city_names = [c['city'] for c in city_pages]
            print(f"  + {len(city_pages)} city pages generated")

    # Generate a mapping file for redirects
    redirect_map = {p['id']: p['slug'] + '.html' for p in generated_pages}
    with open('country-redirects.json', 'w', encoding='utf-8') as f:
        json.dump(redirect_map, f, indent=2)

    print(f"\nGenerated {len(generated_pages)} country pages successfully!")
    print(f"Generated {city_pages_total} city-level pages successfully!")
    print("Redirect map saved to: country-redirects.json")

    # Print summary
    print("\n=== Generated Pages Summary ===")
    total_cities = 0
    for page in generated_pages:
        print(f"  {page['id']}: {page['filename']} ({page['name']}) - {page['cities']} cities, {page['states']} states")
        total_cities += page['cities']
    print(f"\nTotal cities covered: {total_cities}")
    print(f"Total city-level pages: {city_pages_total}")

    return generated_pages


if __name__ == '__main__':
    main()
