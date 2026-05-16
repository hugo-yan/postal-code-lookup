import json
import requests
import zipfile
import io

def get_geonames_available_countries():
    """获取geonames上所有可用的国家列表"""
    try:
        response = requests.get('https://download.geonames.org/export/zip/', timeout=30)
        response.raise_for_status()
        
        # 解析HTML获取所有zip文件
        countries = set()
        for line in response.text.split('\n'):
            if '.zip' in line and 'href' in line:
                # 提取文件名
                start = line.find('href="') + 6
                end = line.find('.zip"', start)
                if start > 5 and end > start:
                    code = line[start:end]
                    # 排除非国家代码的文件
                    if len(code) == 2 and code.isalpha() and code.isupper():
                        countries.add(code)
        
        return sorted(countries)
    except Exception as e:
        print(f"获取geonames列表失败: {e}")
        return []

def check_country_in_geonames(country_code):
    """检查单个国家在geonames上是否有数据"""
    url = f"https://download.geonames.org/export/zip/{country_code}.zip"
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    # 读取现有数据
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    existing_countries = {c['id'] for c in existing_data['countries']}
    
    print("=" * 60)
    print("数据交叉对比报告")
    print("=" * 60)
    
    # 检查geonames上是否有我们现有国家的数据
    print("\n1. 现有国家在 geonames 上的可用性：")
    print("-" * 60)
    
    has_geonames = []
    no_geonames = []
    
    for country_id in sorted(existing_countries):
        available = check_country_in_geonames(country_id)
        status = "[OK] 有数据" if available else "[NO] 无数据"
        print(f"  {country_id}: {status}")
        
        if available:
            has_geonames.append(country_id)
        else:
            no_geonames.append(country_id)
    
    print(f"\n  总结: {len(has_geonames)} 个国家有 geonames 数据")
    print(f"        {len(no_geonames)} 个国家无 geonames 数据: {', '.join(no_geonames)}")
    
    # 检查geonames上有但我们没有的国家
    print("\n2. geonames 上有但我们缺少的国家：")
    print("-" * 60)
    
    geonames_countries = get_geonames_available_countries()
    missing_in_ours = [c for c in geonames_countries if c not in existing_countries]
    
    if missing_in_ours:
        print(f"  共 {len(missing_in_ours)} 个国家:")
        for code in missing_in_ours:
            print(f"    {code}")
    else:
        print("  无")
    
    # 数据质量对比（对已有geonames数据的国家）
    print("\n3. 数据质量对比（geonames vs 现有）：")
    print("-" * 60)
    
    for country_id in has_geonames[:5]:  # 只检查前5个作为示例
        try:
            url = f"https://download.geonames.org/export/zip/{country_id}.zip"
            response = requests.get(url, timeout=30)
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                txt_filename = f"{country_id}.txt"
                with z.open(txt_filename) as f:
                    lines = f.read().decode('utf-8').strip().split('\n')
            
            geonames_count = len(lines)
            
            # 获取现有数据的记录数
            country_data = next(c for c in existing_data['countries'] if c['id'] == country_id)
            existing_count = sum(len(city['postalCodes']) 
                               for state in country_data['states'] 
                               for city in state['cities'])
            
            print(f"  {country_id}: geonames={geonames_count}条, 现有={existing_count}条")
            
        except Exception as e:
            print(f"  {country_id}: 对比失败 - {e}")
    
    print("\n" + "=" * 60)
    print("建议：")
    print("- 对于 geonames 有数据的国家，建议用 geonames 数据替换")
    print("- 对于 geonames 无数据的国家，保留现有数据")
    print("- 可考虑添加 geonames 有但我们缺少的国家")
    print("=" * 60)

if __name__ == '__main__':
    main()
