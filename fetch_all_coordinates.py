import json
import time
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import ssl

# 创建SSL上下文，忽略证书验证（开发环境使用）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def get_coordinates_from_nominatim(city_name, country_code, max_retries=3):
    """使用Nominatim API获取城市坐标"""
    # 国家代码映射（ISO2到ISO3或完整国家名）
    country_names = {
        'US': 'United States', 'CA': 'Canada', 'JP': 'Japan', 'FR': 'France',
        'ZA': 'South Africa', 'UK': 'United Kingdom', 'BR': 'Brazil', 'DE': 'Germany',
        'ID': 'Indonesia', 'PL': 'Poland', 'IT': 'Italy', 'MX': 'Mexico',
        'NO': 'Norway', 'IN': 'India', 'NZ': 'New Zealand', 'AU': 'Australia',
        'RU': 'Russia', 'CN': 'China', 'TR': 'Turkey', 'ES': 'Spain',
        'SE': 'Sweden', 'LT': 'Lithuania', 'GR': 'Greece', 'PR': 'Puerto Rico',
        'TH': 'Thailand', 'FI': 'Finland', 'PT': 'Portugal', 'BE': 'Belgium',
        'DK': 'Denmark', 'HR': 'Croatia', 'NL': 'Netherlands', 'HU': 'Hungary',
        'AT': 'Austria', 'CH': 'Switzerland', 'CZ': 'Czech Republic', 'SK': 'Slovakia',
        'SG': 'Singapore', 'LU': 'Luxembourg', 'IE': 'Ireland', 'IL': 'Israel',
        'KR': 'South Korea', 'MY': 'Malaysia', 'PH': 'Philippines', 'AR': 'Argentina',
        'CL': 'Chile', 'CO': 'Colombia', 'PE': 'Peru', 'EG': 'Egypt',
        'NG': 'Nigeria', 'KE': 'Kenya', 'AE': 'United Arab Emirates', 'SA': 'Saudi Arabia'
    }

    country = country_names.get(country_code, country_code)
    query = f"{city_name}, {country}"
    encoded_query = urllib.parse.quote(query)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1"

    headers = {
        'User-Agent': 'PostalCodeLookup/1.0 ( educational project )'
    }

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data and len(data) > 0:
                    return {
                        'lat': float(data[0]['lat']),
                        'lng': float(data[0]['lon'])
                    }
                return None
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                print(f"  Error fetching {query}: {e}")
                return None

    return None

def fetch_coordinates_for_country(country_data, country_code, delay_between_requests=1.0):
    """为一个国家的所有城市获取坐标"""
    print(f"\n处理国家: {country_code} ({country_data['name']})")
    updated_count = 0
    failed_cities = []

    for state in country_data['states']:
        for city in state['cities']:
            # 如果城市已经有坐标，跳过
            if 'lat' in city and 'lng' in city:
                continue

            city_name = city['name']
            coords = get_coordinates_from_nominatim(city_name, country_code)

            if coords:
                city['lat'] = coords['lat']
                city['lng'] = coords['lng']
                updated_count += 1
                print(f"  ✓ {city_name}: {coords['lat']}, {coords['lng']}")
            else:
                failed_cities.append(city_name)
                print(f"  ✗ {city_name}: 无法获取坐标")

            # 遵守Nominatim使用政策：每秒最多1个请求
            time.sleep(delay_between_requests)

    print(f"  完成: {updated_count} 个城市已更新, {len(failed_cities)} 个失败")
    return updated_count, failed_cities

def fetch_all_coordinates():
    """为所有国家的所有城市获取坐标"""
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_updated = 0
    total_failed = []

    # 优先处理主要国家
    priority_countries = ['CN', 'US', 'UK', 'JP', 'FR', 'DE', 'CA', 'AU', 'IN', 'BR']

    # 先处理优先国家
    for country in data['countries']:
        if country['id'] in priority_countries:
            updated, failed = fetch_coordinates_for_country(country, country['id'])
            total_updated += updated
            total_failed.extend([f"{country['id']}: {c}" for c in failed])

    # 保存中间结果
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n中间结果已保存。已更新 {total_updated} 个城市")

    # 处理其他国家
    for country in data['countries']:
        if country['id'] not in priority_countries:
            updated, failed = fetch_coordinates_for_country(country, country['id'])
            total_updated += updated
            total_failed.extend([f"{country['id']}: {c}" for c in failed])

    # 保存最终结果
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"总计更新: {total_updated} 个城市")
    print(f"失败: {len(total_failed)} 个城市")
    if total_failed:
        print(f"前20个失败的城市:")
        for city in total_failed[:20]:
            print(f"  - {city}")

    return total_updated, total_failed

if __name__ == '__main__':
    print("开始为所有城市获取坐标...")
    print("使用 Nominatim (OpenStreetMap) API")
    print("注意: 这个过程可能需要较长时间，因为API限制每秒1个请求")
    print("="*60)

    fetch_all_coordinates()
