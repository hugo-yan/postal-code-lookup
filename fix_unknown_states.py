import json

def fix_unknown_states():
    """修复所有 'Unknown' 州/省名"""
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for country in data['countries']:
        country_id = country['id']
        for state in country['states']:
            if state['name'] == 'Unknown':
                # 替换为更友好的名称
                state['name'] = 'General'
                print(f"修复 {country_id}: 'Unknown' -> 'General'")
                fixed_count += 1
    
    # 保存修复后的数据
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n共修复 {fixed_count} 个 'Unknown' 州/省名")
    print("数据已保存到 postal_data.json")

if __name__ == '__main__':
    fix_unknown_states()
