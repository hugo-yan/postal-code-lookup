import requests
import zipfile
import io
import json
from collections import defaultdict

def download_country(country_code):
    """下载单个国家的邮编数据"""
    url = f"https://download.geonames.org/export/zip/{country_code}.zip"
    
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            txt_filename = f"{country_code}.txt"
            with z.open(txt_filename) as f:
                content = f.read().decode('utf-8')
        
        # 解析数据
        states = defaultdict(lambda: defaultdict(list))
        
        for line in content.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 7:
                postal_code = parts[1]
                place_name = parts[2]
                state_name = parts[3] if parts[3] else 'Unknown'
                
                states[state_name][place_name].append({
                    'code': postal_code,
                    'area': place_name,
                    'type': 'Standard'
                })
        
        # 转换为所需格式
        country_data = {
            'id': country_code,
            'name': get_country_name(country_code),
            'states': []
        }
        
        state_idx = 0
        for state_name, cities in states.items():
            state_data = {
                'id': f"{country_code}_{state_idx}",
                'name': state_name,
                'cities': []
            }
            
            city_idx = 0
            for city_name, postal_codes in cities.items():
                if city_idx >= 15:
                    break
                
                city_data = {
                    'id': f"{country_code}_{state_idx}_{city_idx}",
                    'name': city_name,
                    'postalCodes': postal_codes[:5]
                }
                state_data['cities'].append(city_data)
                city_idx += 1
            
            country_data['states'].append(state_data)
            state_idx += 1
            if state_idx >= 20:
                break
        
        total_cities = sum(len(s['cities']) for s in country_data['states'])
        total_postal = sum(len(city['postalCodes']) for state in country_data['states'] for city in state['cities'])
        print(f"  {country_code}: {len(country_data['states'])} 州, {total_cities} 城市, {total_postal} 邮编")
        return country_data
        
    except Exception as e:
        print(f"  {country_code}: 失败 - {e}")
        return None

def get_country_name(code):
    names = {
        'US': 'United States', 'CA': 'Canada', 'GB': 'United Kingdom', 'DE': 'Germany',
        'FR': 'France', 'JP': 'Japan', 'CN': 'China', 'IN': 'India', 'AU': 'Australia',
        'BR': 'Brazil', 'IT': 'Italy', 'ES': 'Spain', 'NL': 'Netherlands', 'SE': 'Sweden',
        'NO': 'Norway', 'FI': 'Finland', 'DK': 'Denmark', 'PL': 'Poland', 'AT': 'Austria',
        'CH': 'Switzerland', 'BE': 'Belgium', 'PT': 'Portugal', 'IE': 'Ireland',
        'NZ': 'New Zealand', 'ZA': 'South Africa', 'MX': 'Mexico', 'RU': 'Russia',
        'TR': 'Turkey', 'GR': 'Greece', 'CZ': 'Czech Republic', 'HU': 'Hungary',
        'SK': 'Slovakia', 'HR': 'Croatia', 'SI': 'Slovenia', 'LT': 'Lithuania',
        'LV': 'Latvia', 'EE': 'Estonia', 'LU': 'Luxembourg', 'IS': 'Iceland',
        'MT': 'Malta', 'ID': 'Indonesia', 'SG': 'Singapore', 'TH': 'Thailand',
        'MY': 'Malaysia', 'PH': 'Philippines', 'KR': 'South Korea', 'AE': 'United Arab Emirates',
        'IL': 'Israel', 'UK': 'United Kingdom'
    }
    return names.get(code, code)

def main():
    # 读取现有数据
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    print("开始下载 geonames 数据...")
    print("=" * 60)
    
    updated_count = 0
    
    for i, country in enumerate(existing_data['countries']):
        country_code = country['id']
        download_code = 'GB' if country_code == 'UK' else country_code
        
        print(f"[{i+1}/49] 下载 {country_code}...", end=' ')
        
        data = download_country(download_code)
        if data:
            data['id'] = country_code  # 保持原代码
            existing_data['countries'][i] = data
            updated_count += 1
    
    # 保存
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"完成！更新了 {updated_count}/49 个国家")
    print("数据已保存到 postal_data.json")

if __name__ == '__main__':
    main()
