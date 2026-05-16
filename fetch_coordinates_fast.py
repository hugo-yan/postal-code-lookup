import json
import time

def fetch_coordinates_fast():
    """使用多种方法快速获取城市坐标"""

    try:
        import pgeocode
        print("使用 pgeocode 库获取坐标")
        use_pgeocode = True
    except ImportError:
        print("pgeocode 未安装，将使用内置坐标数据")
        use_pgeocode = False

    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_updated = 0
    total_failed = []
    country_nominatim_cache = {}

    # 首先，加载所有已有的精确坐标（从add_city_coordinates.py添加的）
    print("检查已有坐标...")
    for country in data['countries']:
        for state in country['states']:
            for city in state['cities']:
                if 'lat' in city and 'lng' in city:
                    total_updated += 1

    print(f"已有 {total_updated} 个城市有坐标")

    # 使用pgeocode获取坐标
    if use_pgeocode:
        print("\n使用 pgeocode 获取坐标...")
        for country in data['countries']:
            country_code = country['id']
            print(f"\n处理国家: {country_code}")

            try:
                nomi = pgeocode.Nominatim(country_code)
            except Exception as e:
                print(f"  无法初始化 pgeocode for {country_code}: {e}")
                continue

            country_updated = 0
            for state in country['states']:
                for city in state['cities']:
                    # 跳过已有坐标的城市
                    if 'lat' in city and 'lng' in city:
                        continue

                    city_name = city['name']
                    postal_code = city['postalCodes'][0]['code'] if city['postalCodes'] else None

                    coords = None

                    # 方法1: 使用邮编查询
                    if postal_code:
                        try:
                            result = nomi.query_postal_code(postal_code)
                            if result is not None and not (result.latitude != result.latitude):  # 检查NaN
                                coords = {
                                    'lat': float(result.latitude),
                                    'lng': float(result.longitude)
                                }
                        except Exception:
                            pass

                    # 方法2: 使用城市名查询（如果邮编查询失败）
                    if not coords:
                        try:
                            # pgeocode不支持直接城市名查询，尝试用邮编前缀
                            if postal_code and len(postal_code) >= 2:
                                result = nomi.query_postal_code(postal_code[:2])
                                if result is not None and not (result.latitude != result.latitude):
                                    coords = {
                                        'lat': float(result.latitude),
                                        'lng': float(result.longitude)
                                    }
                        except Exception:
                            pass

                    if coords:
                        city['lat'] = coords['lat']
                        city['lng'] = coords['lng']
                        total_updated += 1
                        country_updated += 1
                    else:
                        total_failed.append(f"{country_code}: {city_name}")

            print(f"  更新了 {country_updated} 个城市")

    # 保存结果
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"总计有坐标的城市: {total_updated}")
    print(f"仍缺少坐标: {len(total_failed)}")

    return total_updated, total_failed

if __name__ == '__main__':
    fetch_coordinates_fast()
