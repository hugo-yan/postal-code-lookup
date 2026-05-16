import json

def add_city_coordinates():
    """为所有国家的城市添加经纬度坐标"""
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 主要城市精确坐标 (lat, lng)
    city_coordinates = {
        # 中国主要城市
        'CN': {
            'Beijing': [39.9042, 116.4074],
            'Shanghai': [31.2304, 121.4737],
            'Guangzhou': [23.1291, 113.2644],
            'Shenzhen': [22.5431, 114.0579],
            'Chengdu': [30.5728, 104.0668],
            'Hangzhou': [30.2741, 120.1551],
            'Wuhan': [30.5928, 114.3055],
            'Xi\'an': [34.3416, 108.9398],
            'Nanjing': [32.0603, 118.7969],
            'Chongqing': [29.5630, 106.5516],
            'Tianjin': [39.0842, 117.2009],
            'Suzhou': [31.2989, 120.5853],
            'Dalian': [38.9140, 121.6147],
            'Qingdao': [36.0671, 120.3826],
            'Zhengzhou': [34.7466, 113.6253],
        },
        # 美国主要城市
        'US': {
            'New York': [40.7128, -74.0060],
            'Los Angeles': [34.0522, -118.2437],
            'Chicago': [41.8781, -87.6298],
            'Houston': [29.7604, -95.3698],
            'San Francisco': [37.7749, -122.4194],
            'Seattle': [47.6062, -122.3321],
            'Miami': [25.7617, -80.1918],
            'Boston': [42.3601, -71.0589],
            'Las Vegas': [36.1699, -115.1398],
            'Denver': [39.7392, -104.9903],
            'Washington': [38.9072, -77.0369],
            'Philadelphia': [39.9526, -75.1652],
            'Atlanta': [33.7490, -84.3880],
            'Dallas': [32.7767, -96.7970],
            'San Diego': [32.7157, -117.1611],
            'Austin': [30.2672, -97.7431],
            'Portland': [45.5152, -122.6784],
            'Phoenix': [33.4484, -112.0740],
            'Detroit': [42.3314, -83.0458],
            'Minneapolis': [44.9778, -93.2650],
        },
        # 英国主要城市
        'UK': {
            'London': [51.5074, -0.1278],
            'Manchester': [53.4808, -2.2426],
            'Birmingham': [52.4862, -1.8904],
            'Glasgow': [55.8609, -4.2514],
            'Edinburgh': [55.9533, -3.1883],
            'Liverpool': [53.4084, -2.9916],
            'Bristol': [51.4545, -2.5879],
            'Leeds': [53.8008, -1.5491],
            'Sheffield': [53.3811, -1.4701],
            'Cardiff': [51.4816, -3.1791],
            'Belfast': [54.5973, -5.9301],
            'Newcastle': [54.9783, -1.6178],
            'Nottingham': [52.9548, -1.1581],
            'Leicester': [52.6369, -1.1398],
            'Coventry': [52.4068, -1.5197],
        },
        # 日本
        'JP': {
            'Tokyo': [35.6762, 139.6503],
            'Osaka': [34.6937, 135.5023],
            'Yokohama': [35.4437, 139.6380],
            'Nagoya': [35.1815, 136.9066],
            'Sapporo': [43.0618, 141.3545],
            'Fukuoka': [33.5902, 130.4017],
            'Kobe': [34.6901, 135.1955],
            'Kyoto': [35.0116, 135.7681],
        },
        # 法国
        'FR': {
            'Paris': [48.8566, 2.3522],
            'Marseille': [43.2965, 5.3698],
            'Lyon': [45.7640, 4.8357],
            'Toulouse': [43.6047, 1.4442],
            'Nice': [43.7102, 7.2620],
            'Nantes': [47.2184, -1.5536],
            'Strasbourg': [48.5734, 7.7521],
        },
        # 德国
        'DE': {
            'Berlin': [52.5200, 13.4050],
            'Hamburg': [53.5511, 9.9937],
            'Munich': [48.1351, 11.5820],
            'Cologne': [50.9375, 6.9603],
            'Frankfurt': [50.1109, 8.6821],
            'Stuttgart': [48.7758, 9.1829],
            'Dusseldorf': [51.2277, 6.7735],
        },
        # 加拿大
        'CA': {
            'Toronto': [43.6532, -79.3832],
            'Vancouver': [49.2827, -123.1207],
            'Montreal': [45.5017, -73.5673],
            'Calgary': [51.0447, -114.0719],
            'Ottawa': [45.4215, -75.6972],
            'Edmonton': [53.5461, -113.4938],
        },
        # 澳大利亚
        'AU': {
            'Sydney': [-33.8688, 151.2093],
            'Melbourne': [-37.8136, 144.9631],
            'Brisbane': [-27.4698, 153.0251],
            'Perth': [-31.9505, 115.8605],
            'Adelaide': [-34.9285, 138.6007],
        },
        # 印度
        'IN': {
            'Mumbai': [19.0760, 72.8777],
            'Delhi': [28.6139, 77.2090],
            'Bangalore': [12.9716, 77.5946],
            'Chennai': [13.0827, 80.2707],
            'Kolkata': [22.5726, 88.3639],
            'Hyderabad': [17.3850, 78.4867],
        },
        # 巴西
        'BR': {
            'Sao Paulo': [-23.5505, -46.6333],
            'Rio de Janeiro': [-22.9068, -43.1729],
            'Brasilia': [-15.7975, -47.8919],
            'Salvador': [-12.9777, -38.5016],
        },
        # 俄罗斯
        'RU': {
            'Moscow': [55.7558, 37.6173],
            'Saint Petersburg': [59.9311, 30.3609],
            'Novosibirsk': [55.0084, 82.9357],
        },
        # 意大利
        'IT': {
            'Rome': [41.9028, 12.4964],
            'Milan': [45.4642, 9.1900],
            'Naples': [40.8518, 14.2681],
            'Turin': [45.0703, 7.6869],
        },
        # 西班牙
        'ES': {
            'Madrid': [40.4168, -3.7038],
            'Barcelona': [41.3851, 2.1734],
            'Valencia': [39.4699, -0.3763],
            'Seville': [37.3891, -5.9845],
        },
        # 墨西哥
        'MX': {
            'Mexico City': [19.4326, -99.1332],
            'Guadalajara': [20.6597, -103.3496],
            'Monterrey': [25.6866, -100.3161],
        },
        # 韩国 (South Korea)
        'KR': {
            'Seoul': [37.5665, 126.9780],
            'Busan': [35.1796, 129.0756],
            'Incheon': [37.4563, 126.7052],
        },
        # 荷兰
        'NL': {
            'Amsterdam': [52.3676, 4.9041],
            'Rotterdam': [51.9244, 4.4777],
            'The Hague': [52.0705, 4.3007],
        },
        # 瑞士
        'CH': {
            'Zurich': [47.3769, 8.5417],
            'Geneva': [46.2044, 6.1432],
            'Bern': [46.9480, 7.4474],
        },
        # 瑞典
        'SE': {
            'Stockholm': [59.3293, 18.0686],
            'Gothenburg': [57.7089, 11.9746],
            'Malmö': [55.6050, 13.0038],
        },
        # 挪威
        'NO': {
            'Oslo': [59.9139, 10.7522],
            'Bergen': [60.3913, 5.3221],
        },
        # 丹麦
        'DK': {
            'Copenhagen': [55.6761, 12.5683],
            'Aarhus': [56.1629, 10.2039],
        },
        # 芬兰
        'FI': {
            'Helsinki': [60.1699, 24.9384],
            'Espoo': [60.2055, 24.6559],
        },
        # 比利时
        'BE': {
            'Brussels': [50.8503, 4.3517],
            'Antwerp': [51.2194, 4.4025],
        },
        # 奥地利
        'AT': {
            'Vienna': [48.2082, 16.3738],
            'Salzburg': [47.8095, 13.0550],
        },
        # 波兰
        'PL': {
            'Warsaw': [52.2297, 21.0122],
            'Krakow': [50.0647, 19.9450],
        },
        # 土耳其
        'TR': {
            'Istanbul': [41.0082, 28.9784],
            'Ankara': [39.9334, 32.8597],
        },
        # 泰国
        'TH': {
            'Bangkok': [13.7563, 100.5018],
            'Chiang Mai': [18.7883, 98.9853],
        },
        # 新加坡
        'SG': {
            'Singapore': [1.3521, 103.8198],
        },
        # 新西兰
        'NZ': {
            'Auckland': [-36.8509, 174.7645],
            'Wellington': [-41.2865, 174.7762],
        },
        # 南非
        'ZA': {
            'Cape Town': [-33.9249, 18.4241],
            'Johannesburg': [-26.2041, 28.0473],
            'Durban': [-29.8587, 31.0218],
        },
        # 印度尼西亚
        'ID': {
            'Jakarta': [-6.2088, 106.8456],
            'Surabaya': [-7.2575, 112.7521],
        },
        # 葡萄牙
        'PT': {
            'Lisbon': [38.7223, -9.1393],
            'Porto': [41.1579, -8.6291],
        },
        # 希腊
        'GR': {
            'Athens': [37.9838, 23.7275],
            'Thessaloniki': [40.6401, 22.9444],
        },
        # 捷克
        'CZ': {
            'Prague': [50.0755, 14.4378],
            'Brno': [49.1951, 16.6068],
        },
        # 匈牙利
        'HU': {
            'Budapest': [47.4979, 19.0402],
        },
        # 爱尔兰
        'IE': {
            'Dublin': [53.3498, -6.2603],
        },
        # 以色列
        'IL': {
            'Tel Aviv': [32.0853, 34.7818],
            'Jerusalem': [31.7683, 35.2137],
        },
        # 马来西亚
        'MY': {
            'Kuala Lumpur': [3.1390, 101.6869],
        },
        # 菲律宾
        'PH': {
            'Manila': [14.5995, 120.9842],
        },
        # 阿根廷
        'AR': {
            'Buenos Aires': [-34.6037, -58.3816],
        },
        # 智利
        'CL': {
            'Santiago': [-33.4489, -70.6693],
        },
        # 哥伦比亚
        'CO': {
            'Bogota': [4.7110, -74.0721],
        },
        # 秘鲁
        'PE': {
            'Lima': [-12.0464, -77.0428],
        },
        # 埃及
        'EG': {
            'Cairo': [30.0444, 31.2357],
        },
        # 尼日利亚
        'NG': {
            'Lagos': [6.5244, 3.3792],
        },
        # 肯尼亚
        'KE': {
            'Nairobi': [-1.2921, 36.8219],
        },
        # 阿联酋
        'AE': {
            'Dubai': [25.2048, 55.2708],
            'Abu Dhabi': [24.4539, 54.3773],
        },
        # 沙特阿拉伯
        'SA': {
            'Riyadh': [24.7136, 46.6753],
            'Jeddah': [21.4858, 39.1925],
        },
    }

    updated_count = 0
    missing_coords = []

    for country in data['countries']:
        country_code = country['id']
        coords_map = city_coordinates.get(country_code, {})

        for state in country['states']:
            for city in state['cities']:
                city_name = city['name']
                if city_name in coords_map:
                    city['lat'] = coords_map[city_name][0]
                    city['lng'] = coords_map[city_name][1]
                    updated_count += 1
                else:
                    missing_coords.append(f"{country_code}: {city_name}")

    # 保存更新后的数据
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已为 {updated_count} 个城市添加坐标")
    print(f"缺少坐标的城市数量: {len(missing_coords)}")

    if missing_coords:
        print("\n前20个缺少坐标的城市:")
        for city in missing_coords[:20]:
            print(f"  - {city}")

    return updated_count, missing_coords

if __name__ == '__main__':
    add_city_coordinates()
