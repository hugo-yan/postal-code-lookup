import pgeocode
import json

def extract_country_data(country_code):
    """提取单个国家的邮编数据"""
    try:
        nomi = pgeocode.Nominatim(country_code)
        data = nomi._data
        
        if data.empty:
            print(f"警告: {country_code} 没有数据")
            return None
        
        # 按州/省分组
        states = {}
        for _, row in data.iterrows():
            state_name = row.get('state_name', 'Unknown')
            state_code = row.get('state_code', 'UNK')
            place_name = row.get('place_name', 'Unknown')
            postal_code = row.get('postal_code', '')
            
            if state_code not in states:
                states[state_code] = {
                    'name': state_name,
                    'cities': {}
                }
            
            if place_name not in states[state_code]['cities']:
                states[state_code]['cities'][place_name] = []
            
            states[state_code]['cities'][place_name].append({
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
        
        for state_code, state_info in states.items():
            state_data = {
                'id': state_code,
                'name': state_info['name'],
                'cities': []
            }
            
            # 每个州最多取10个城市
            city_count = 0
            for city_name, postal_codes in state_info['cities'].items():
                if city_count >= 10:
                    break
                
                city_data = {
                    'id': f"{country_code}_{state_code}_{city_count}",
                    'name': city_name,
                    'postalCodes': postal_codes[:5]  # 每个城市最多5个邮编
                }
                state_data['cities'].append(city_data)
                city_count += 1
            
            country_data['states'].append(state_data)
        
        print(f"成功提取 {country_code} 数据: {len(states)} 个州/省")
        return country_data
        
    except Exception as e:
        print(f"提取 {country_code} 数据失败: {e}")
        return None

def get_country_name(country_code):
    """获取国家名称"""
    country_names = {
        'US': 'United States',
        'CA': 'Canada',
        'GB': 'United Kingdom',
        'DE': 'Germany',
        'FR': 'France',
        'JP': 'Japan',
        'CN': 'China',
        'IN': 'India',
        'AU': 'Australia',
        'BR': 'Brazil',
        'IT': 'Italy',
        'ES': 'Spain',
        'NL': 'Netherlands',
        'SE': 'Sweden',
        'NO': 'Norway',
        'FI': 'Finland',
        'DK': 'Denmark',
        'PL': 'Poland',
        'AT': 'Austria',
        'CH': 'Switzerland',
        'BE': 'Belgium',
        'PT': 'Portugal',
        'IE': 'Ireland',
        'NZ': 'New Zealand',
        'ZA': 'South Africa',
        'MX': 'Mexico',
        'RU': 'Russia',
        'TR': 'Turkey',
        'GR': 'Greece',
        'CZ': 'Czech Republic',
        'HU': 'Hungary',
        'SK': 'Slovakia',
        'HR': 'Croatia',
        'SI': 'Slovenia',
        'LT': 'Lithuania',
        'LV': 'Latvia',
        'EE': 'Estonia',
        'LU': 'Luxembourg',
        'IS': 'Iceland',
        'MT': 'Malta',
        'CY': 'Cyprus',
        'BG': 'Bulgaria',
        'RO': 'Romania',
        'RS': 'Serbia',
        'BA': 'Bosnia and Herzegovina',
        'ME': 'Montenegro',
        'MK': 'North Macedonia',
        'AL': 'Albania',
        'MD': 'Moldova',
        'BY': 'Belarus',
        'UA': 'Ukraine',
        'GE': 'Georgia',
        'AM': 'Armenia',
        'AZ': 'Azerbaijan',
        'KZ': 'Kazakhstan',
        'UZ': 'Uzbekistan',
        'KG': 'Kyrgyzstan',
        'TJ': 'Tajikistan',
        'TM': 'Turkmenistan',
        'MN': 'Mongolia',
        'KP': 'North Korea',
        'KR': 'South Korea',
        'TW': 'Taiwan',
        'HK': 'Hong Kong',
        'MO': 'Macau',
        'VN': 'Vietnam',
        'TH': 'Thailand',
        'MY': 'Malaysia',
        'SG': 'Singapore',
        'ID': 'Indonesia',
        'PH': 'Philippines',
        'KH': 'Cambodia',
        'LA': 'Laos',
        'MM': 'Myanmar',
        'BD': 'Bangladesh',
        'NP': 'Nepal',
        'BT': 'Bhutan',
        'LK': 'Sri Lanka',
        'MV': 'Maldives',
        'PK': 'Pakistan',
        'AF': 'Afghanistan',
        'IR': 'Iran',
        'IQ': 'Iraq',
        'SY': 'Syria',
        'LB': 'Lebanon',
        'JO': 'Jordan',
        'IL': 'Israel',
        'PS': 'Palestine',
        'SA': 'Saudi Arabia',
        'YE': 'Yemen',
        'OM': 'Oman',
        'AE': 'United Arab Emirates',
        'QA': 'Qatar',
        'BH': 'Bahrain',
        'KW': 'Kuwait',
        'EG': 'Egypt',
        'LY': 'Libya',
        'TN': 'Tunisia',
        'DZ': 'Algeria',
        'MA': 'Morocco',
        'MR': 'Mauritania',
        'ML': 'Mali',
        'NE': 'Niger',
        'TD': 'Chad',
        'SD': 'Sudan',
        'ER': 'Eritrea',
        'DJ': 'Djibouti',
        'ET': 'Ethiopia',
        'SO': 'Somalia',
        'KE': 'Kenya',
        'UG': 'Uganda',
        'TZ': 'Tanzania',
        'RW': 'Rwanda',
        'BI': 'Burundi',
        'CD': 'Democratic Republic of the Congo',
        'CG': 'Republic of the Congo',
        'GA': 'Gabon',
        'GQ': 'Equatorial Guinea',
        'ST': 'Sao Tome and Principe',
        'CM': 'Cameroon',
        'CF': 'Central African Republic',
        'NG': 'Nigeria',
        'BJ': 'Benin',
        'TG': 'Togo',
        'GH': 'Ghana',
        'CI': 'Ivory Coast',
        'LR': 'Liberia',
        'SL': 'Sierra Leone',
        'GN': 'Guinea',
        'GW': 'Guinea-Bissau',
        'GM': 'Gambia',
        'SN': 'Senegal',
        'CV': 'Cape Verde',
        'BF': 'Burkina Faso'
    }
    return country_names.get(country_code, country_code)

def main():
    # 主要国家列表（40个核心国家）
    countries = [
        'US', 'CA', 'GB', 'DE', 'FR', 'JP', 'CN', 'IN', 'AU', 'BR',
        'IT', 'ES', 'NL', 'SE', 'NO', 'FI', 'DK', 'PL', 'AT', 'CH',
        'BE', 'PT', 'IE', 'NZ', 'ZA', 'MX', 'RU', 'TR', 'GR', 'CZ',
        'HU', 'SK', 'HR', 'SI', 'LT', 'LV', 'EE', 'LU', 'IS', 'MT'
    ]
    
    all_data = []
    
    print("开始提取邮编数据...")
    for country in countries:
        data = extract_country_data(country)
        if data:
            all_data.append(data)
    
    # 保存为JSON
    output = {
        'countries': all_data
    }
    
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！共提取 {len(all_data)} 个国家的数据")
    print("数据已保存到 postal_data.json")

if __name__ == '__main__':
    main()
