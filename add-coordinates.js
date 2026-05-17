// 为热门城市添加坐标数据
const fs = require('fs');

// 读取 mockData.js
let dataContent = fs.readFileSync('mockData.js', 'utf8');

// 热门城市坐标数据 (城市名 -> {lat, lng})
const cityCoordinates = {
  // 日本
  "Tokyo": { lat: 35.6762, lng: 139.6503 },
  "Osaka": { lat: 34.6937, lng: 135.5023 },
  "Kyoto": { lat: 35.0116, lng: 135.7681 },
  "Yokohama": { lat: 35.4437, lng: 139.6380 },
  "Nagoya": { lat: 35.1815, lng: 136.9066 },
  "Sapporo": { lat: 43.0618, lng: 141.3545 },
  "Fukuoka": { lat: 33.5902, lng: 130.4017 },
  "Kobe": { lat: 34.6901, lng: 135.1955 },
  
  // 印度
  "Mumbai": { lat: 19.0760, lng: 72.8777 },
  "Delhi": { lat: 28.6139, lng: 77.2090 },
  "Bangalore": { lat: 12.9716, lng: 77.5946 },
  "Chennai": { lat: 13.0827, lng: 80.2707 },
  "Kolkata": { lat: 22.5726, lng: 88.3639 },
  "Hyderabad": { lat: 17.3850, lng: 78.4867 },
  "Pune": { lat: 18.5204, lng: 73.8567 },
  "Ahmedabad": { lat: 23.0225, lng: 72.5714 },
  
  // 巴西
  "Sao Paulo": { lat: -23.5505, lng: -46.6333 },
  "Rio de Janeiro": { lat: -22.9068, lng: -43.1729 },
  "Brasilia": { lat: -15.7975, lng: -47.8919 },
  "Salvador": { lat: -12.9714, lng: -38.5014 },
  "Fortaleza": { lat: -3.7319, lng: -38.5267 },
  "Belo Horizonte": { lat: -19.9167, lng: -43.9345 },
  
  // 意大利
  "Rome": { lat: 41.9028, lng: 12.4964 },
  "Milan": { lat: 45.4642, lng: 9.1900 },
  "Naples": { lat: 40.8518, lng: 14.2681 },
  "Turin": { lat: 45.0703, lng: 7.6869 },
  "Palermo": { lat: 38.1157, lng: 13.3615 },
  "Genoa": { lat: 44.4056, lng: 8.9463 },
  "Bologna": { lat: 44.4949, lng: 11.3426 },
  "Florence": { lat: 43.7696, lng: 11.2558 },
  "Venice": { lat: 45.4408, lng: 12.3155 },
  
  // 西班牙
  "Valencia": { lat: 39.4699, lng: -0.3763 },
  "Seville": { lat: 37.3891, lng: -5.9845 },
  "Zaragoza": { lat: 41.6488, lng: -0.8891 },
  "Malaga": { lat: 36.7213, lng: -4.4214 },
  "Murcia": { lat: 37.9922, lng: -1.1307 },
  
  // 荷兰
  "Amsterdam": { lat: 52.3676, lng: 4.9041 },
  "Rotterdam": { lat: 51.9244, lng: 4.4777 },
  "The Hague": { lat: 52.0705, lng: 4.3007 },
  "Utrecht": { lat: 52.0907, lng: 5.1214 },
  "Eindhoven": { lat: 51.4416, lng: 5.4697 },
  
  // 瑞典
  "Gothenburg": { lat: 57.7089, lng: 11.9746 },
  "Malmö": { lat: 55.6050, lng: 13.0038 },
  "Uppsala": { lat: 59.8586, lng: 17.6389 },
  
  // 丹麦
  "Copenhagen": { lat: 55.6761, lng: 12.5683 },
  "Aarhus": { lat: 56.1629, lng: 10.2039 },
  "Odense": { lat: 55.4038, lng: 10.4024 },
  
  // 波兰
  "Warsaw": { lat: 52.2297, lng: 21.0122 },
  "Krakow": { lat: 50.0647, lng: 19.9450 },
  "Lodz": { lat: 51.7592, lng: 19.4560 },
  "Wroclaw": { lat: 51.1079, lng: 17.0385 },
  "Poznan": { lat: 52.4064, lng: 16.9252 },
  "Gdansk": { lat: 54.3520, lng: 18.6466 },
  
  // 奥地利
  "Vienna": { lat: 48.2082, lng: 16.3738 },
  "Graz": { lat: 47.0707, lng: 15.4395 },
  "Linz": { lat: 48.3069, lng: 14.2858 },
  "Salzburg": { lat: 47.8095, lng: 13.0550 },
  "Innsbruck": { lat: 47.2692, lng: 11.4041 },
  
  // 瑞士
  "Zurich": { lat: 47.3769, lng: 8.5417 },
  "Geneva": { lat: 46.2044, lng: 6.1432 },
  "Basel": { lat: 47.5596, lng: 7.5886 },
  "Bern": { lat: 46.9480, lng: 7.4474 },
  "Lausanne": { lat: 46.5197, lng: 6.6323 },
  
  // 比利时
  "Brussels": { lat: 50.8503, lng: 4.3517 },
  "Antwerp": { lat: 51.2194, lng: 4.4025 },
  "Ghent": { lat: 51.0543, lng: 3.7174 },
  "Bruges": { lat: 51.2093, lng: 3.2247 },
  "Liege": { lat: 50.6326, lng: 5.5797 },
  
  // 葡萄牙
  "Lisbon": { lat: 38.7223, lng: -9.1393 },
  "Porto": { lat: 41.1579, lng: -8.6291 },
  "Braga": { lat: 41.5454, lng: -8.4265 },
  "Faro": { lat: 37.0194, lng: -7.9304 },
  
  // 爱尔兰
  "Dublin": { lat: 53.3498, lng: -6.2603 },
  "Cork": { lat: 51.8985, lng: -8.4756 },
  "Galway": { lat: 53.2707, lng: -9.0568 },
  
  // 新西兰
  "Auckland": { lat: -36.8485, lng: 174.7633 },
  "Wellington": { lat: -41.2865, lng: 174.7762 },
  "Christchurch": { lat: -43.5321, lng: 172.6362 },
  
  // 南非
  "Johannesburg": { lat: -26.2041, lng: 28.0473 },
  "Cape Town": { lat: -33.9249, lng: 18.4241 },
  "Durban": { lat: -29.8587, lng: 31.0218 },
  "Pretoria": { lat: -25.7479, lng: 28.2293 },
  
  // 墨西哥
  "Mexico City": { lat: 19.4326, lng: -99.1332 },
  "Guadalajara": { lat: 20.6597, lng: -103.3496 },
  "Monterrey": { lat: 25.6866, lng: -100.3161 },
  "Puebla": { lat: 19.0414, lng: -98.2063 },
  "Tijuana": { lat: 32.5149, lng: -117.0382 },
  
  // 俄罗斯
  "Moscow": { lat: 55.7558, lng: 37.6173 },
  "Saint Petersburg": { lat: 59.9311, lng: 30.3609 },
  "Novosibirsk": { lat: 55.0084, lng: 82.9357 },
  "Yekaterinburg": { lat: 56.8389, lng: 60.6057 },
  "Kazan": { lat: 55.8304, lng: 49.0661 },
  
  // 土耳其
  "Istanbul": { lat: 41.0082, lng: 28.9784 },
  "Ankara": { lat: 39.9334, lng: 32.8597 },
  "Izmir": { lat: 38.4192, lng: 27.1287 },
  "Antalya": { lat: 36.8969, lng: 30.7133 },
  "Bursa": { lat: 40.1826, lng: 29.0669 },
  
  // 捷克
  "Prague": { lat: 50.0755, lng: 14.4378 },
  "Brno": { lat: 49.1951, lng: 16.6068 },
  "Ostrava": { lat: 49.8209, lng: 18.2625 },
  
  // 匈牙利
  "Budapest": { lat: 47.4979, lng: 19.0402 },
  "Debrecen": { lat: 47.5316, lng: 21.6273 },
  "Szeged": { lat: 46.2530, lng: 20.1414 },
  
  // 斯洛伐克
  "Bratislava": { lat: 48.1486, lng: 17.1077 },
  "Kosice": { lat: 48.7164, lng: 21.2611 },
  
  // 克罗地亚
  "Zagreb": { lat: 45.8150, lng: 15.9819 },
  "Split": { lat: 43.5081, lng: 16.4402 },
  "Rijeka": { lat: 45.3271, lng: 14.4422 },
  
  // 斯洛文尼亚
  "Ljubljana": { lat: 46.0569, lng: 14.5058 },
  "Maribor": { lat: 46.5547, lng: 15.6459 },
  
  // 立陶宛
  "Vilnius": { lat: 54.6872, lng: 25.2797 },
  "Kaunas": { lat: 54.8985, lng: 23.9036 },
  "Klaipeda": { lat: 55.7033, lng: 21.1443 },
  
  // 拉脱维亚
  "Riga": { lat: 56.9496, lng: 24.1052 },
  "Daugavpils": { lat: 55.8758, lng: 26.5362 },
  
  // 爱沙尼亚
  "Tallinn": { lat: 59.4370, lng: 24.7536 },
  "Tartu": { lat: 58.3780, lng: 26.7281 },
  
  // 卢森堡
  "Luxembourg": { lat: 49.6116, lng: 6.1319 },
  
  // 冰岛
  "Reykjavik": { lat: 64.1466, lng: -21.9426 },
  
  // 马耳他
  "Valletta": { lat: 35.8989, lng: 14.5146 },
  
  // 加拿大
  "Toronto": { lat: 43.6532, lng: -79.3832 },
  "Vancouver": { lat: 49.2827, lng: -123.1207 },
  "Montreal": { lat: 45.5017, lng: -73.5673 },
  "Calgary": { lat: 51.0447, lng: -114.0719 },
  "Ottawa": { lat: 45.4215, lng: -75.6972 },
  "Edmonton": { lat: 53.5461, lng: -113.4938 },
  "Quebec City": { lat: 46.8139, lng: -71.2080 },
  "Winnipeg": { lat: 49.8951, lng: -97.1384 },
  
  // 澳大利亚
  "Sydney": { lat: -33.8688, lng: 151.2093 },
  "Melbourne": { lat: -37.8136, lng: 144.9631 },
  "Brisbane": { lat: -27.4698, lng: 153.0251 },
  "Perth": { lat: -31.9505, lng: 115.8605 },
  "Canberra": { lat: -35.2809, lng: 149.1300 },
  
  // 新加坡
  "Singapore": { lat: 1.3521, lng: 103.8198 },
  
  // 泰国
  "Bangkok": { lat: 13.7563, lng: 100.5018 },
  "Chiang Mai": { lat: 18.7883, lng: 98.9853 },
  "Phuket": { lat: 7.8804, lng: 98.3923 },
  "Pattaya": { lat: 12.9236, lng: 100.8825 },
  
  // 马来西亚
  "Kuala Lumpur": { lat: 3.1390, lng: 101.6869 },
  "George Town": { lat: 5.4141, lng: 100.3288 },
  "Johor Bahru": { lat: 1.4927, lng: 103.7414 },
  "Kota Kinabalu": { lat: 5.9804, lng: 116.0735 },
  "Kuching": { lat: 1.5535, lng: 110.3593 },
  
  // 菲律宾
  "Manila": { lat: 14.5995, lng: 120.9842 },
  "Cebu City": { lat: 10.3157, lng: 123.8854 },
  "Davao City": { lat: 7.1907, lng: 125.4553 },
  
  // 韩国
  "Seoul": { lat: 37.5665, lng: 126.9780 },
  "Busan": { lat: 35.1796, lng: 129.0756 },
  "Incheon": { lat: 37.4563, lng: 126.7052 },
  "Daegu": { lat: 35.8714, lng: 128.6014 },
  
  // 阿联酋
  "Dubai": { lat: 25.2048, lng: 55.2708 },
  "Abu Dhabi": { lat: 24.4539, lng: 54.3773 },
  "Sharjah": { lat: 25.3463, lng: 55.4209 },
  
  // 印度尼西亚
  "Jakarta": { lat: -6.2088, lng: 106.8456 },
  "Surabaya": { lat: -7.2575, lng: 112.7521 },
  "Bandung": { lat: -6.9175, lng: 107.6191 },
  "Medan": { lat: 3.5952, lng: 98.6722 },
  
  // 希腊
  "Athens": { lat: 37.9838, lng: 23.7275 },
  "Thessaloniki": { lat: 40.6401, lng: 22.9444 },
  "Patras": { lat: 38.2466, lng: 21.7346 },
  "Heraklion": { lat: 35.3387, lng: 25.1442 },
  
  // 中国更多城市
  "Tianjin": { lat: 39.0842, lng: 117.2010 },
  "Suzhou": { lat: 31.2989, lng: 120.5853 },
  "Qingdao": { lat: 36.0671, lng: 120.3826 },
  "Dalian": { lat: 38.9140, lng: 121.6147 },
  "Xiamen": { lat: 24.4798, lng: 118.0894 },
  "Ningbo": { lat: 29.8683, lng: 121.5440 },
  "Wuxi": { lat: 31.4912, lng: 120.3119 },
  "Fuzhou": { lat: 26.0745, lng: 119.2965 },
  "Jinan": { lat: 36.6512, lng: 117.1201 },
  "Harbin": { lat: 45.8038, lng: 126.5350 },
  "Changchun": { lat: 43.8171, lng: 125.3235 },
  "Shenyang": { lat: 41.8057, lng: 123.4315 },
  "Shijiazhuang": { lat: 38.0428, lng: 114.5149 },
  "Taiyuan": { lat: 37.8706, lng: 112.5489 },
  "Kunming": { lat: 25.0389, lng: 102.7183 },
  "Guiyang": { lat: 26.6477, lng: 106.6302 },
  "Nanning": { lat: 22.8170, lng: 108.3665 },
  "Lanzhou": { lat: 36.0611, lng: 103.8343 },
  "Haikou": { lat: 20.0440, lng: 110.1999 },
  "Urumqi": { lat: 43.8256, lng: 87.6168 },
  "Lhasa": { lat: 29.6500, lng: 91.1000 },
  "Yinchuan": { lat: 38.4872, lng: 106.2309 },
  "Xining": { lat: 36.6171, lng: 101.7782 },
  "Hohhot": { lat: 40.8414, lng: 111.7519 },
  "Hefei": { lat: 31.8206, lng: 117.2272 },
  "Nanchang": { lat: 28.6820, lng: 115.8579 },
  "Changsha": { lat: 28.2282, lng: 112.9388 },
  "Kunshan": { lat: 31.3890, lng: 120.9543 },
  "Zhuhai": { lat: 22.2710, lng: 113.5670 },
  
  // 英国更多城市
  "Manchester": { lat: 53.4808, lng: -2.2426 },
  "Birmingham": { lat: 52.4862, lng: -1.8904 },
  "Leeds": { lat: 53.8008, lng: -1.5491 },
  "Glasgow": { lat: 55.8609, lng: -4.2514 },
  "Sheffield": { lat: 53.3811, lng: -1.4701 },
  "Liverpool": { lat: 53.4084, lng: -2.9916 },
  "Edinburgh": { lat: 55.9533, lng: -3.1883 },
  "Bristol": { lat: 51.4545, lng: -2.5879 },
  "Cardiff": { lat: 51.4816, lng: -3.1791 },
  "Belfast": { lat: 54.5973, lng: -5.9301 },
  "Newcastle": { lat: 54.9783, lng: -1.6178 },
  
  // 德国更多城市
  "Hamburg": { lat: 53.5511, lng: 9.9937 },
  "Munich": { lat: 48.1351, lng: 11.5820 },
  "Cologne": { lat: 50.9375, lng: 6.9603 },
  "Frankfurt": { lat: 50.1109, lng: 8.6821 },
  "Stuttgart": { lat: 48.7758, lng: 9.1829 },
  "Düsseldorf": { lat: 51.2277, lng: 6.7735 },
  "Dortmund": { lat: 51.5136, lng: 7.4653 },
  "Essen": { lat: 51.4556, lng: 7.0116 },
  "Leipzig": { lat: 51.3397, lng: 12.3731 },
  "Bremen": { lat: 53.0793, lng: 8.8017 },
  "Dresden": { lat: 51.0504, lng: 13.7373 },
  "Hanover": { lat: 52.3759, lng: 9.7320 },
  "Nuremberg": { lat: 49.4521, lng: 11.0767 },
  
  // 法国更多城市
  "Marseille": { lat: 43.2965, lng: 5.3698 },
  "Lyon": { lat: 45.7640, lng: 4.8357 },
  "Toulouse": { lat: 43.6047, lng: 1.4442 },
  "Nice": { lat: 43.7102, lng: 7.2620 },
  "Bordeaux": { lat: 44.8378, lng: -0.5792 },
  "Lille": { lat: 50.6292, lng: 3.0573 },
  "Strasbourg": { lat: 48.5734, lng: 7.7521 },
  
  // 美国更多城市
  "Philadelphia": { lat: 39.9526, lng: -75.1652 },
  "Phoenix": { lat: 33.4484, lng: -112.0740 },
  "San Antonio": { lat: 29.4241, lng: -98.4936 },
  "San Diego": { lat: 32.7157, lng: -117.1611 },
  "Dallas": { lat: 32.7767, lng: -96.7970 },
  "San Jose": { lat: 37.3382, lng: -121.8863 },
  "Austin": { lat: 30.2672, lng: -97.7431 },
  "Jacksonville": { lat: 30.3322, lng: -81.6557 },
  "Columbus": { lat: 39.9612, lng: -82.9988 },
  "Charlotte": { lat: 35.2271, lng: -80.8431 },
  "Indianapolis": { lat: 39.7684, lng: -86.1581 },
  "Detroit": { lat: 42.3314, lng: -83.0458 },
  "Nashville": { lat: 36.1627, lng: -86.7816 },
  "Portland": { lat: 45.5152, lng: -122.6784 },
  "Oklahoma City": { lat: 35.4676, lng: -97.5164 },
  "Memphis": { lat: 35.1495, lng: -90.0490 },
  "Louisville": { lat: 38.2527, lng: -85.7585 },
  "Baltimore": { lat: 39.2904, lng: -76.6122 },
  "Milwaukee": { lat: 43.0389, lng: -87.9065 },
  "Albuquerque": { lat: 35.0844, lng: -106.6504 },
  "Tucson": { lat: 32.2226, lng: -110.9747 },
  "Sacramento": { lat: 38.5816, lng: -121.4944 },
  "Kansas City": { lat: 39.0997, lng: -94.5786 },
  "Atlanta": { lat: 33.7490, lng: -84.3880 },
  "Raleigh": { lat: 35.7796, lng: -78.6382 },
  "Omaha": { lat: 41.2565, lng: -95.9345 },
  "Minneapolis": { lat: 44.9778, lng: -93.2650 },
  "Cleveland": { lat: 41.4993, lng: -81.6944 },
  "Virginia Beach": { lat: 36.8529, lng: -75.9780 },
  "New Orleans": { lat: 29.9511, lng: -90.0715 },
  "Honolulu": { lat: 21.3099, lng: -157.8581 }
};

// 统计信息
let addedCount = 0;
let skippedCount = 0;
const addedCities = [];
const skippedCities = [];

// 为每个城市添加坐标
for (const [cityName, coords] of Object.entries(cityCoordinates)) {
  // 构建正则表达式来查找城市（需要匹配 name: "CityName" 且后面没有 lat:）
  const regex = new RegExp(`(name: "${cityName}", postalCodes: \\[[^\\]]*\\])(?!\\s*, lat:)`, 'g');
  
  if (regex.test(dataContent)) {
    // 重置 lastIndex
    regex.lastIndex = 0;
    
    // 替换添加坐标
    dataContent = dataContent.replace(regex, `$1, lat: ${coords.lat}, lng: ${coords.lng}`);
    addedCount++;
    addedCities.push(cityName);
  } else {
    skippedCount++;
    skippedCities.push(cityName);
  }
}

// 保存修改后的文件
fs.writeFileSync('mockData.js', dataContent);

// 输出报告
console.log('='.repeat(60));
console.log('坐标添加报告');
console.log('='.repeat(60));
console.log(`\n✅ 成功添加坐标: ${addedCount} 个城市`);
console.log(`⏭️  跳过（已存在或不存在）: ${skippedCount} 个城市`);
console.log(`\n已添加坐标的城市 (${addedCount}个):`);
addedCities.forEach(city => console.log(`  - ${city}`));

if (skippedCities.length > 0) {
  console.log(`\n跳过的城市 (${skippedCount}个):`);
  skippedCities.forEach(city => console.log(`  - ${city}`));
}

console.log('\n' + '='.repeat(60));
console.log('✅ 坐标数据已成功添加到 mockData.js');
console.log('='.repeat(60));
