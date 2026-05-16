import json

def convert_to_mockdata():
    # 读取提取的数据
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    countries = data['countries']
    
    # 生成 mockData.js 内容
    lines = []
    lines.append('const postalData = {')
    lines.append('  countries: [')
    
    for i, country in enumerate(countries):
        lines.append(f'    {{')
        lines.append(f'      id: "{country["id"]}",')
        lines.append(f'      name: "{country["name"]}",')
        lines.append(f'      states: [')
        
        for j, state in enumerate(country['states']):
            # 跳过无效的州数据
            if str(state['id']).lower() == 'nan' or str(state['name']).lower() == 'nan':
                continue
            lines.append(f'        {{ id: "{state["id"]}", name: "{state["name"]}", cities: [')
            
            for k, city in enumerate(state['cities']):
                postal_codes_str = ', '.join([
                    f'{{ code: "{pc["code"]}", area: "{pc["area"]}", type: "{pc["type"]}" }}'
                    for pc in city['postalCodes']
                ])
                coords_str = ''
                if 'lat' in city and 'lng' in city:
                    coords_str = f', lat: {city["lat"]}, lng: {city["lng"]}'
                lines.append(f'          {{ id: "{city["id"]}", name: "{city["name"]}", postalCodes: [{postal_codes_str}]{coords_str} }}')
                if k < len(state['cities']) - 1:
                    lines[-1] += ','
            
            lines.append('        ]}')
            if j < len(country['states']) - 1:
                lines[-1] += ','
        
        lines.append('      ]')
        lines.append('    }')
        if i < len(countries) - 1:
            lines[-1] += ','
    
    lines.append('  ]')
    lines.append('};')
    lines.append('')
    lines.append('// 国家代码到名称的映射')
    lines.append('const countryNames = {')
    for i, country in enumerate(countries):
        comma = ',' if i < len(countries) - 1 else ''
        lines.append(f'  "{country["id"]}": "{country["name"]}"{comma}')
    lines.append('};')
    lines.append('')
    lines.append('// 获取国家数据')
    lines.append('function getCountryData(countryCode) {')
    lines.append('  return postalData.countries.find(c => c.id === countryCode);')
    lines.append('}')
    lines.append('')
    lines.append('// 获取所有国家列表')
    lines.append('function getAllCountries() {')
    lines.append('  return postalData.countries;')
    lines.append('}')
    lines.append('')
    lines.append('// 搜索邮编')
    lines.append('function searchPostalCode(countryCode, query) {')
    lines.append('  const country = getCountryData(countryCode);')
    lines.append('  if (!country) return [];')
    lines.append('  ')
    lines.append('  const results = [];')
    lines.append('  country.states.forEach(state => {')
    lines.append('    state.cities.forEach(city => {')
    lines.append('      city.postalCodes.forEach(pc => {')
    lines.append('        if (pc.code.includes(query) || pc.area.toLowerCase().includes(query.toLowerCase())) {')
    lines.append('          results.push({')
    lines.append('            state: state.name,')
    lines.append('            city: city.name,')
    lines.append('            code: pc.code,')
    lines.append('            area: pc.area,')
    lines.append('            type: pc.type')
    lines.append('          });')
    lines.append('        }')
    lines.append('      });')
    lines.append('    });')
    lines.append('  });')
    lines.append('  ')
    lines.append('  return results;')
    lines.append('}')
    lines.append('')
    lines.append('// 导出数据（用于模块化环境）')
    lines.append('if (typeof module !== "undefined" && module.exports) {')
    lines.append('  module.exports = { postalData, countryNames, getCountryData, getAllCountries, searchPostalCode };')
    lines.append('}')
    
    # 写入文件
    with open('mockData.js', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"转换完成！共 {len(countries)} 个国家")
    print("数据已保存到 mockData.js")

if __name__ == '__main__':
    convert_to_mockdata()
