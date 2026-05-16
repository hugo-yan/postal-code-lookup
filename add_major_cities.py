import json

def add_major_cities():
    """添加主要城市到数据中"""
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 主要城市数据
    major_cities = {
        'CN': [
            {'name': 'Beijing', 'state': 'Beijing', 'postal': '100000'},
            {'name': 'Shanghai', 'state': 'Shanghai', 'postal': '200000'},
            {'name': 'Guangzhou', 'state': 'Guangdong', 'postal': '510000'},
            {'name': 'Shenzhen', 'state': 'Guangdong', 'postal': '518000'},
            {'name': 'Chengdu', 'state': 'Sichuan', 'postal': '610000'},
            {'name': 'Hangzhou', 'state': 'Zhejiang', 'postal': '310000'},
            {'name': 'Wuhan', 'state': 'Hubei', 'postal': '430000'},
            {'name': 'Xi\'an', 'state': 'Shaanxi', 'postal': '710000'},
            {'name': 'Nanjing', 'state': 'Jiangsu', 'postal': '210000'},
            {'name': 'Chongqing', 'state': 'Chongqing', 'postal': '400000'},
        ],
        'US': [
            {'name': 'New York', 'state': 'New York', 'postal': '10001'},
            {'name': 'Los Angeles', 'state': 'California', 'postal': '90001'},
            {'name': 'Chicago', 'state': 'Illinois', 'postal': '60601'},
            {'name': 'Houston', 'state': 'Texas', 'postal': '77001'},
            {'name': 'San Francisco', 'state': 'California', 'postal': '94102'},
            {'name': 'Seattle', 'state': 'Washington', 'postal': '98101'},
            {'name': 'Miami', 'state': 'Florida', 'postal': '33101'},
            {'name': 'Boston', 'state': 'Massachusetts', 'postal': '02101'},
            {'name': 'Las Vegas', 'state': 'Nevada', 'postal': '89101'},
            {'name': 'Denver', 'state': 'Colorado', 'postal': '80201'},
        ],
        'UK': [
            {'name': 'London', 'state': 'England', 'postal': 'SW1A'},
            {'name': 'Manchester', 'state': 'England', 'postal': 'M1'},
            {'name': 'Birmingham', 'state': 'England', 'postal': 'B1'},
            {'name': 'Glasgow', 'state': 'Scotland', 'postal': 'G1'},
            {'name': 'Edinburgh', 'state': 'Scotland', 'postal': 'EH1'},
            {'name': 'Liverpool', 'state': 'England', 'postal': 'L1'},
            {'name': 'Bristol', 'state': 'England', 'postal': 'BS1'},
            {'name': 'Leeds', 'state': 'England', 'postal': 'LS1'},
            {'name': 'Sheffield', 'state': 'England', 'postal': 'S1'},
            {'name': 'Cardiff', 'state': 'Wales', 'postal': 'CF1'},
        ]
    }
    
    added_count = 0
    
    for country_code, cities in major_cities.items():
        country = next((c for c in data['countries'] if c['id'] == country_code), None)
        if not country:
            print(f"Country {country_code} not found")
            continue
        
        for city_data in cities:
            # 检查城市是否已存在
            exists = False
            for state in country['states']:
                for city in state['cities']:
                    if city['name'] == city_data['name']:
                        exists = True
                        break
                if exists:
                    break
            
            if exists:
                print(f"  {city_data['name']} already exists in {country_code}")
                continue
            
            # 查找或创建州/省
            state = next((s for s in country['states'] if s['name'] == city_data['state']), None)
            if not state:
                # 创建新州/省
                state_idx = len(country['states'])
                state = {
                    'id': f"{country_code}_{state_idx}",
                    'name': city_data['state'],
                    'cities': []
                }
                country['states'].append(state)
                print(f"  Created new state: {city_data['state']}")
            
            # 添加城市
            city_idx = len(state['cities'])
            city = {
                'id': f"{state['id']}_{city_idx}",
                'name': city_data['name'],
                'postalCodes': [
                    {'code': city_data['postal'], 'area': city_data['name'], 'type': 'Standard'}
                ]
            }
            state['cities'].append(city)
            added_count += 1
            print(f"  Added {city_data['name']} to {country_code}")
    
    # 保存更新后的数据
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n共添加 {added_count} 个主要城市")
    print("数据已保存到 postal_data.json")

if __name__ == '__main__':
    add_major_cities()
