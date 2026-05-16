import json

with open('postal_data.json', encoding='utf-8') as f:
    data = json.load(f)

for code in ['CN', 'US', 'UK']:
    country = next((c for c in data['countries'] if c['id'] == code), None)
    if country:
        print(f"\n{code} - {country['name']}:")
        print(f"  States: {len(country['states'])}")
        all_cities = []
        for state in country['states']:
            for city in state['cities']:
                all_cities.append(city['name'])
        print(f"  Total cities: {len(all_cities)}")
        print(f"  First 10: {all_cities[:10]}")
        # Check for specific cities
        targets = {
            'CN': ['Beijing', 'Shanghai', 'Guangzhou'],
            'US': ['New York', 'Los Angeles', 'Chicago'],
            'UK': ['London', 'Manchester', 'Birmingham']
        }
        for target in targets.get(code, []):
            found = target in all_cities
            print(f"  {target}: {'FOUND' if found else 'NOT FOUND'}")
