import json
import requests
import time
from urllib.parse import urlencode

class PostalCodeTester:
    def __init__(self, base_url="http://localhost:8081"):
        self.base_url = base_url
        self.results = []
        
        # 测试用例数据
        self.test_cases = {
            'CN': {
                'name': 'China',
                'cities': [
                    {'name': 'Beijing', 'expected_postal': '100000'},
                    {'name': 'Shanghai', 'expected_postal': '200000'},
                    {'name': 'Guangzhou', 'expected_postal': '510000'},
                    {'name': 'Shenzhen', 'expected_postal': '518000'},
                    {'name': 'Chengdu', 'expected_postal': '610000'},
                ]
            },
            'US': {
                'name': 'United States',
                'cities': [
                    {'name': 'New York', 'expected_postal': '10001'},
                    {'name': 'Los Angeles', 'expected_postal': '90001'},
                    {'name': 'Chicago', 'expected_postal': '60601'},
                    {'name': 'Houston', 'expected_postal': '77001'},
                    {'name': 'San Francisco', 'expected_postal': '94102'},
                ]
            },
            'UK': {
                'name': 'United Kingdom',
                'cities': [
                    {'name': 'London', 'expected_postal': 'SW1A'},
                    {'name': 'Manchester', 'expected_postal': 'M1'},
                    {'name': 'Birmingham', 'expected_postal': 'B1'},
                    {'name': 'Glasgow', 'expected_postal': 'G1'},
                    {'name': 'Edinburgh', 'expected_postal': 'EH1'},
                ]
            }
        }
    
    def test_page_load(self, country_code):
        """测试页面加载"""
        url = f"{self.base_url}/country.html?country={country_code}"
        try:
            response = requests.get(url, timeout=10)
            success = response.status_code == 200
            return {
                'test': 'Page Load',
                'url': url,
                'success': success,
                'status_code': response.status_code,
                'error': None if success else f"Status code: {response.status_code}"
            }
        except Exception as e:
            return {
                'test': 'Page Load',
                'url': url,
                'success': False,
                'status_code': None,
                'error': str(e)
            }
    
    def test_data_file(self, country_code):
        """测试数据文件是否存在且包含该国家数据"""
        try:
            with open('mockData.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含国家数据
            has_data = f"id: '{country_code}'" in content or f'id: "{country_code}"' in content
            
            return {
                'test': 'Data File Check',
                'success': has_data,
                'error': None if has_data else f"Country {country_code} not found in mockData.js"
            }
        except Exception as e:
            return {
                'test': 'Data File Check',
                'success': False,
                'error': str(e)
            }
    
    def test_postal_data_structure(self, country_code):
        """测试邮编数据结构"""
        try:
            with open('postal_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            country = next((c for c in data['countries'] if c['id'] == country_code), None)
            if not country:
                return {
                    'test': 'Postal Data Structure',
                    'success': False,
                    'error': f"Country {country_code} not found in postal_data.json"
                }
            
            # 检查结构
            issues = []
            if not country.get('states'):
                issues.append("No states data")
            else:
                for state in country['states']:
                    if not state.get('cities'):
                        issues.append(f"State {state.get('name', 'UNKNOWN')} has no cities")
                    else:
                        for city in state['cities']:
                            if not city.get('postalCodes'):
                                issues.append(f"City {city.get('name', 'UNKNOWN')} has no postal codes")
            
            return {
                'test': 'Postal Data Structure',
                'success': len(issues) == 0,
                'states_count': len(country.get('states', [])),
                'cities_count': sum(len(s.get('cities', [])) for s in country.get('states', [])),
                'error': '; '.join(issues) if issues else None
            }
        except Exception as e:
            return {
                'test': 'Postal Data Structure',
                'success': False,
                'error': str(e)
            }
    
    def test_city_search(self, country_code, city_name):
        """测试城市搜索功能"""
        try:
            with open('postal_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            country = next((c for c in data['countries'] if c['id'] == country_code), None)
            if not country:
                return {
                    'test': f'City Search: {city_name}',
                    'success': False,
                    'error': f"Country {country_code} not found"
                }
            
            # 搜索城市
            found = False
            postal_code = None
            for state in country['states']:
                for city in state['cities']:
                    if city['name'].lower() == city_name.lower():
                        found = True
                        postal_code = city['postalCodes'][0]['code'] if city['postalCodes'] else None
                        break
                if found:
                    break
            
            return {
                'test': f'City Search: {city_name}',
                'success': found,
                'postal_code': postal_code,
                'error': None if found else f"City {city_name} not found"
            }
        except Exception as e:
            return {
                'test': f'City Search: {city_name}',
                'success': False,
                'error': str(e)
            }
    
    def test_map_integration(self, country_code):
        """测试地图集成"""
        url = f"{self.base_url}/country.html?country={country_code}"
        try:
            response = requests.get(url, timeout=10)
            content = response.text
            
            # 检查是否包含 Leaflet
            has_leaflet_css = 'leaflet' in content.lower()
            has_leaflet_js = 'leaflet' in content.lower()
            has_map_div = 'id="map"' in content
            
            success = has_leaflet_css and has_leaflet_js and has_map_div
            
            return {
                'test': 'Map Integration',
                'success': success,
                'has_leaflet_css': has_leaflet_css,
                'has_leaflet_js': has_leaflet_js,
                'has_map_div': has_map_div,
                'error': None if success else "Missing Leaflet or map container"
            }
        except Exception as e:
            return {
                'test': 'Map Integration',
                'success': False,
                'error': str(e)
            }
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 70)
        print("邮编查询系统测试报告")
        print("=" * 70)
        print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试国家: 中国 (CN), 美国 (US), 英国 (UK)")
        print("=" * 70)
        
        all_results = []
        
        for country_code, country_data in self.test_cases.items():
            print(f"\n【{country_data['name']} ({country_code})】")
            print("-" * 50)
            
            country_results = []
            
            # 1. 测试页面加载
            result = self.test_page_load(country_code)
            country_results.append(result)
            self.print_result(result)
            
            # 2. 测试数据文件
            result = self.test_data_file(country_code)
            country_results.append(result)
            self.print_result(result)
            
            # 3. 测试数据结构
            result = self.test_postal_data_structure(country_code)
            country_results.append(result)
            self.print_result(result)
            
            # 4. 测试城市搜索
            for city in country_data['cities']:
                result = self.test_city_search(country_code, city['name'])
                country_results.append(result)
                self.print_result(result)
                time.sleep(0.1)  # 避免请求过快
            
            # 5. 测试地图集成
            result = self.test_map_integration(country_code)
            country_results.append(result)
            self.print_result(result)
            
            all_results.extend(country_results)
        
        # 生成总结
        self.print_summary(all_results)
        
        return all_results
    
    def print_result(self, result):
        """打印单个测试结果"""
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"  {status} - {result['test']}")
        if result.get('error'):
            print(f"       错误: {result['error']}")
        if 'postal_code' in result:
            print(f"       邮编: {result['postal_code']}")
        if 'states_count' in result:
            print(f"       州/省: {result['states_count']}, 城市: {result['cities_count']}")
    
    def print_summary(self, results):
        """打印测试总结"""
        total = len(results)
        passed = sum(1 for r in results if r['success'])
        failed = total - passed
        
        print("\n" + "=" * 70)
        print("测试总结")
        print("=" * 70)
        print(f"总测试数: {total}")
        print(f"通过: {passed} ({passed/total*100:.1f}%)")
        print(f"失败: {failed} ({failed/total*100:.1f}%)")
        
        if failed > 0:
            print("\n失败的测试:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['test']}: {result.get('error', 'Unknown error')}")
        
        print("=" * 70)

if __name__ == '__main__':
    tester = PostalCodeTester()
    tester.run_all_tests()
