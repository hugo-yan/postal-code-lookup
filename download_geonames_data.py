import requests
import zipfile
import io
import json
import csv
from collections import defaultdict

def download_and_parse_country(country_code):
    """下载并解析单个国家的邮编数据"""
    url = f"https://download.geonames.org/export/zip/{country_code}.zip"
    
    try:
        print(f"正在下载 {country_code} 的数据...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 解压 ZIP 文件
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # 读取 txt 文件
            txt_filename = f"{country_code}.txt"
            with z.open(txt_filename) as f:
                content = f.read().decode('utf-8')
        
        # 解析数据
        states = defaultdict(lambda: defaultdict(list))
        
        for line in content.strip().split('\n'):
            parts = line.split('\t')
            if len(parts) >= 7:
                country = parts[0]
                postal_code = parts[1]
                place_name = parts[2]
                state_name = parts[3] if parts[3] else 'Unknown'
                state_code = parts[4] if parts[4] else 'UNK'
                
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
                if city_idx >= 10:  # 每个州最多10个城市
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
            if state_idx >= 15:  # 每个国家最多15个州
                break
        
        print(f"成功解析 {country_code}: {len(country_data['states'])} 个州/省, {sum(len(s['cities']) for s in country_data['states'])} 个城市")
        return country_data
        
    except Exception as e:
        print(f"下载/解析 {country_code} 失败: {e}")
        return None

def get_country_name(code):
    """获取国家名称"""
    names = {
        'CN': 'China',
        'GB': 'United Kingdom',
        'ID': 'Indonesia',
        'GR': 'Greece',
        'SG': 'Singapore',
        'TH': 'Thailand',
        'MY': 'Malaysia',
        'PH': 'Philippines',
        'KR': 'South Korea',
        'AE': 'United Arab Emirates',
        'IL': 'Israel'
    }
    return names.get(code, code)

def main():
    # 需要下载的国家列表
    countries = ['CN', 'GB', 'ID', 'GR', 'SG', 'TH', 'MY', 'PH', 'KR', 'AE', 'IL']
    
    all_data = []
    
    for country in countries:
        data = download_and_parse_country(country)
        if data:
            all_data.append(data)
    
    # 保存为JSON
    output = {'countries': all_data}
    
    with open('geonames_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！共下载 {len(all_data)} 个国家的数据")
    print("数据已保存到 geonames_data.json")

if __name__ == '__main__':
    main()
