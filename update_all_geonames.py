import requests
import zipfile
import io
import json
from collections import defaultdict
import time

def download_and_parse_country(country_code):
    """下载并解析单个国家的邮编数据"""
    url = f"https://download.geonames.org/export/zip/{country_code}.zip"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        # 解压 ZIP 文件
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            txt_filename = f"{country_code}.txt"
            with z.open(txt_filename) as f:
                content = f.read().decode('utf-8')
        
        # 解析数据 - 按州/省分组，每个州最多15个城市，每个城市最多5个邮编
        states = defaultdict(lambda: defaultdict(list))
        
        for line in content.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 7:
                country = parts[0]
                postal_code = parts[1]
                place_name = parts[2]
                state_name = parts[3] if parts[3] else 'Unknown'
                
                # 添加到州/省 -> 城市 -> 邮编结构
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
                if city_idx >= 15:  # 每个州最多15个城市
                    break
                
                city_data = {
                    'id': f"{country_code}_{state_idx}_{city_idx}",
                    'name': city_name,
                    'postalCodes': postal_codes[:5]  # 每个城市最多5个邮编
                }
                state_data['cities'].append(city_data)
                city_idx += 1
            
            country_data['states'].append(state_data)
            state_idx += 1
            if state_idx >= 20:  # 每个国家最多20个州
                break
        
        total_cities = sum(len(s['cities']) for s in country_data['states'])
        total_postal = sum(len(city['postalCodes']) for state in country_data['states'] for city in state['cities'])
        print(f"  {country_code}: {len(country_data['states'])} 州/省, {total_cities} 城市, {total_postal} 邮编")
        return country_data
        
    except Exception as e:
        print(f"  {country_code}: 下载失败 - {e}")
        return None

def get_country_name(code):
    """获取国家名称"""
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
    # 读取现有数据获取国家列表
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    existing_countries = [c['id'] for c in existing_data['countries']]
    
    print("=" * 60)
    print("开始下载 geonames 数据替换所有国家")
    print("=" * 60)
    
    all_data = []
    failed = []
    
    for country_code in existing_countries:
        # 处理 UK -> GB 的映射
        download_code = 'GB' if country_code == 'UK' else country_code
        
        data = download_and_parse_country(download_code)
        if data:
            # 保持原来的国家代码
            data['id'] = country_code
            all_data.append(data)
        else:
            # 如果下载失败，保留原有数据
            original = next(c for c in existing_data['countries'] if c['id'] == country_code)
            all_data.append(original)
            failed.append(country_code)
        
        time.sleep(0.5)  # 避免请求过快
    
    # 保存更新后的数据
    output = {'countries': all_data}
    
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"完成！共处理 {len(all_data)} 个国家")
    if failed:
        print(f"下载失败保留原数据: {', '.join(failed)}")
    print("数据已保存到 postal_data.json")
    print("=" * 60)

if __name__ == '__main__':
    main()
