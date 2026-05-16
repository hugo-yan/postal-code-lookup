import json

def merge_geonames_data():
    # 读取现有数据
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # 读取 geonames 数据
    with open('geonames_data.json', 'r', encoding='utf-8') as f:
        geonames_data = json.load(f)
    
    # 创建现有数据的ID映射
    existing_ids = {c['id']: i for i, c in enumerate(existing_data['countries'])}
    
    # 需要替换的国家代码映射（GB -> UK）
    code_mapping = {
        'GB': 'UK'  # geonames用GB，但我们用UK
    }
    
    replaced = []
    added = []
    
    for country in geonames_data['countries']:
        country_id = country['id']
        
        # 处理代码映射
        if country_id in code_mapping:
            country['id'] = code_mapping[country_id]
            country_id = country['id']
        
        if country_id in existing_ids:
            # 替换现有数据
            idx = existing_ids[country_id]
            existing_data['countries'][idx] = country
            replaced.append(country_id)
        else:
            # 添加新数据
            existing_data['countries'].append(country)
            added.append(country_id)
    
    # 保存更新后的数据
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"已替换 {len(replaced)} 个国家的数据: {', '.join(replaced)}")
    print(f"已添加 {len(added)} 个国家的数据: {', '.join(added)}")
    print(f"现在共有 {len(existing_data['countries'])} 个国家")

if __name__ == '__main__':
    merge_geonames_data()
