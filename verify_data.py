import json
import requests

def check_country_data(country_data):
    """检查单个国家的数据问题"""
    issues = []
    country_id = country_data['id']
    
    # 1. 检查基本结构
    if not country_data.get('states'):
        issues.append("缺少州/省数据")
        return issues
    
    # 2. 检查每个州
    for state in country_data['states']:
        state_name = state.get('name', 'UNKNOWN')
        
        # 检查州名是否为 "nan" 或 "Unknown"
        if state_name.lower() in ['nan', 'unknown', '']:
            issues.append(f"州/省名无效: '{state_name}'")
        
        # 检查城市
        if not state.get('cities'):
            issues.append(f"州 '{state_name}' 缺少城市数据")
            continue
        
        for city in state['cities']:
            city_name = city.get('name', 'UNKNOWN')
            
            # 检查城市名
            if city_name.lower() in ['nan', 'unknown', '']:
                issues.append(f"城市名无效: '{city_name}' (在州 '{state_name}' 中)")
            
            # 检查邮编
            if not city.get('postalCodes'):
                issues.append(f"城市 '{city_name}' 缺少邮编数据")
            else:
                for pc in city['postalCodes']:
                    code = pc.get('code', '')
                    if not code or code.lower() in ['nan', 'unknown']:
                        issues.append(f"邮编无效: '{code}' (城市: {city_name})")
    
    return issues

def verify_all_data():
    """验证所有国家数据"""
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 70)
    print("国家数据完整性验证报告")
    print("=" * 70)
    
    total_countries = len(data['countries'])
    problematic_countries = 0
    summary = []
    
    for country in data['countries']:
        country_id = country['id']
        country_name = country.get('name', 'UNKNOWN')
        states_count = len(country.get('states', []))
        cities_count = sum(len(s.get('cities', [])) for s in country.get('states', []))
        postal_count = sum(
            len(city.get('postalCodes', [])) 
            for state in country.get('states', []) 
            for city in state.get('cities', [])
        )
        
        issues = check_country_data(country)
        
        if issues:
            problematic_countries += 1
            print(f"\n[{country_id}] {country_name}")
            print(f"  州/省: {states_count}, 城市: {cities_count}, 邮编: {postal_count}")
            print(f"  问题:")
            for issue in issues[:5]:  # 只显示前5个问题
                print(f"    - {issue}")
            if len(issues) > 5:
                print(f"    ... 还有 {len(issues) - 5} 个问题")
            summary.append({
                'id': country_id,
                'name': country_name,
                'issues': len(issues),
                'states': states_count,
                'cities': cities_count,
                'postal': postal_count
            })
        else:
            print(f"[{country_id}] {country_name} - OK (州:{states_count}, 城:{cities_count}, 邮编:{postal_count})")
    
    print("\n" + "=" * 70)
    print(f"总结: {problematic_countries}/{total_countries} 个国家有问题")
    
    if summary:
        print("\n问题国家列表:")
        for s in summary:
            print(f"  {s['id']} ({s['name']}): {s['issues']} 个问题")
    
    print("=" * 70)
    
    return summary

def check_geonames_availability():
    """检查哪些国家在 geonames 上有数据"""
    print("\n" + "=" * 70)
    print("Geonames 数据源可用性检查")
    print("=" * 70)
    
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    no_geonames = []
    has_geonames = []
    
    for country in data['countries']:
        country_id = country['id']
        download_code = 'GB' if country_id == 'UK' else country_id
        
        url = f"https://download.geonames.org/export/zip/{download_code}.zip"
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                has_geonames.append(country_id)
            else:
                no_geonames.append(country_id)
        except:
            no_geonames.append(country_id)
    
    print(f"有 geonames 数据: {len(has_geonames)} 个国家")
    print(f"无 geonames 数据: {len(no_geonames)} 个国家 - {', '.join(no_geonames)}")
    
    return no_geonames

if __name__ == '__main__':
    summary = verify_all_data()
    no_geonames = check_geonames_availability()
    
    print("\n" + "=" * 70)
    print("建议修复方案:")
    print("=" * 70)
    
    if summary:
        print("1. 数据质量问题:")
        print("   - 对于 'nan' 或 'Unknown' 的数据，需要清理或替换")
        print("   - 对于缺少城市或邮编的州/省，需要补充数据")
    
    if no_geonames:
        print("\n2. 无 geonames 数据源的国家:")
        print(f"   - {', '.join(no_geonames)}")
        print("   - 建议: 使用模拟数据或寻找其他数据源")
    
    print("\n3. 数据完整性建议:")
    print("   - 检查所有国家的州/省数量是否合理")
    print("   - 确保每个城市都有有效的邮编数据")
    print("   - 验证国家代码和名称的对应关系")
