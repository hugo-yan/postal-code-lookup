#!/usr/bin/env python3
"""
Generate static HTML pages for each country
This improves SEO by creating static URLs like /us-postal-code.html
instead of dynamic URLs like /country.html?country=US
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


def generate_static_page(country_id, country_data):
    """Generate a static HTML page for a country"""
    slug = COUNTRY_SLUGS.get(country_id, f"{country_id.lower()}-postal-code")
    display_name = COUNTRY_NAMES.get(country_id, country_data['name'])
    flag_code = FLAG_CODE_MAP.get(country_id, country_id.lower())
    coords = DEFAULT_COORDS.get(country_id, [0, 0])

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
                'lat': city.get('lat'),
                'lng': city.get('lng'),
            })

    cities.sort(key=lambda x: x['name'])
    states.sort()

    # Generate city options HTML
    city_options = '\n'.join([
        f'          <option value="{c["id"]}">{c["name"]} ({c["state"]})</option>'
        for c in cities[:150]  # Limit to 150 cities for performance
    ])

    # Generate state links HTML
    state_links = '\n'.join([
        f'          <a href="#{state.replace(" ", "-").lower()}" class="state-link">{state}</a>'
        for state in states[:50]  # Limit to 50 states
    ])

    # Generate popular cities list (first 30)
    popular_cities = cities[:30]
    popular_cities_html = '\n'.join([
        f'        <div class="city-link-item">{c["name"]} ({c["state"]})</div>'
        for c in popular_cities
    ])

    # Generate Schema.org structured data
    schema_data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{display_name} Postal Code Lookup",
        "description": f"Search postal codes and zip codes for cities in {display_name}. Find postal code information by city name or address.",
        "url": f"https://postalcodelookup.info/{slug}.html",
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i + 1,
                    "name": f"{c['name']} Postal Code",
                    "description": f"Postal code for {c['name']}, {display_name}"
                }
                for i, c in enumerate(popular_cities[:10])
            ]
        }
    }

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">

  <title>{display_name} Postal Code Lookup | Find Zip Codes in {display_name}</title>
  <meta name="description" content="Search postal codes and zip codes for cities in {display_name}. Find {display_name} postal code information by city name or address. Free lookup tool with map.">
  <meta name="keywords" content="{display_name.lower()} postal code, {display_name.lower()} zip code, {display_name.lower()} postcode, postal code lookup {display_name.lower()}, {display_name.lower()} address lookup">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://postalcodelookup.info/{slug}.html">

  <meta property="og:type" content="website">
  <meta property="og:title" content="{display_name} Postal Code Lookup | Find Zip Codes in {display_name}">
  <meta property="og:description" content="Search postal codes for cities in {display_name}. Free lookup tool with interactive map.">
  <meta property="og:url" content="https://postalcodelookup.info/{slug}.html">

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%231E40AF' width='100' height='100' rx='20'/%3E%3Ctext x='50' y='68' font-size='50' text-anchor='middle' fill='white' font-family='Arial' font-weight='bold'%3EP%3C/text%3E%3C/svg%3E">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="country.css">

  <!-- Leaflet CSS for Map -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>

  <script type="application/ld+json">
  {json.dumps(schema_data, indent=2)}
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
      <!-- Top Section: Search + About -->
      <div class="top-section">
        <!-- Left: Search Tool -->
        <section class="search-tool" aria-labelledby="search-heading">
          <div class="search-tool-header">
            <img id="search-country-flag" class="search-country-flag" src="flags/{flag_code}.png" alt="{display_name} flag" width="24" height="18">
            <h1 id="search-heading" class="search-tool-title">
              {display_name} Postal Code Lookup
            </h1>
          </div>

          <div class="search-box">
            <label for="city-search" class="form-label">Enter Address / Place / Location / City</label>
            <div class="autocomplete-wrapper">
              <svg class="form-input-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
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
              This is an online tool to search postal code of a place, address or city in {display_name}.
              Select the name of the Place/Address/City (in {display_name}) from the suggested list.
              This will display the postal code of the selected location from {display_name} on the map.
            </p>
            <p><strong>Note that the postal code may be searched with nearby approximation.</strong></p>
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
            <select id="cities-select" class="cities-select">
              <option value="">Select a city...</option>
{city_options}
            </select>
          </div>

          <button id="show-selected-btn" class="show-btn">
            Show Postal Code
          </button>

          <!-- Popular Cities Links for SEO -->
          <div class="popular-cities-links" style="margin-top: 1.5rem;">
            <h3 style="font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: 0.75rem;">Popular {display_name} Cities:</h3>
            <div class="city-links-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.5rem;">
{popular_cities_html}
            </div>
          </div>
        </section>

        <!-- Right: State/Province List -->
        <section class="states-list" aria-labelledby="states-heading">
          <h2 id="states-heading" class="states-title">State/Province level Postal Code Search:</h2>
          <div id="states-container" class="states-container">
{state_links}
          </div>
        </section>
      </div>
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

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

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


def parse_mock_data():
    """Parse the mockData.js file to extract country information"""
    with open('mockData.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the countries array
    match = re.search(r'const postalData = ({.*?});', content, re.DOTALL)
    if not match:
        print("Could not find postalData in mockData.js")
        return []

    # Use a safer approach - extract country IDs and names
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


def main():
    """Main function to generate all static pages"""
    print("Starting static page generation...")

    # Parse mock data to get country list
    countries = parse_mock_data()
    print(f"Found {len(countries)} countries in mockData.js")

    generated_pages = []

    for country in countries:
        country_id = country['id']
        country_name = country['name']

        # Skip duplicates (UK/GB)
        if country_id == 'GB':
            continue

        # Create minimal country data for page generation
        country_data = {
            'name': country_name,
            'states': []  # We'll populate this from the JS file
        }

        slug, html = generate_static_page(country_id, country_data)
        filename = f"{slug}.html"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        generated_pages.append({
            'id': country_id,
            'name': country_name,
            'slug': slug,
            'filename': filename
        })
        print(f"Generated: {filename} ({country_name})")

    # Generate a mapping file for redirects
    redirect_map = {p['id']: p['slug'] + '.html' for p in generated_pages}
    with open('country-redirects.json', 'w', encoding='utf-8') as f:
        json.dump(redirect_map, f, indent=2)

    print(f"\nGenerated {len(generated_pages)} static pages successfully!")
    print("Redirect map saved to: country-redirects.json")

    # Print summary
    print("\n=== Generated Pages ===")
    for page in generated_pages:
        print(f"  {page['id']}: {page['filename']} ({page['name']})")

    return generated_pages


if __name__ == '__main__':
    main()
