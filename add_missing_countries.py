import json

def add_missing_countries():
    # 读取现有数据
    with open('postal_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_ids = {c['id'] for c in data['countries']}
    
    # 缺失国家的模拟数据
    missing_countries = [
        {
            "id": "UK",
            "name": "United Kingdom",
            "states": [
                {
                    "id": "ENG",
                    "name": "England",
                    "cities": [
                        {"id": "UK_ENG_0", "name": "London", "postalCodes": [{"code": "SW1A 1AA", "area": "Westminster", "type": "Standard"}, {"code": "EC1A 1BB", "area": "City of London", "type": "Standard"}]},
                        {"id": "UK_ENG_1", "name": "Manchester", "postalCodes": [{"code": "M1 1AA", "area": "Manchester City Centre", "type": "Standard"}, {"code": "M2 1AA", "area": "Manchester", "type": "Standard"}]},
                        {"id": "UK_ENG_2", "name": "Birmingham", "postalCodes": [{"code": "B1 1AA", "area": "Birmingham City Centre", "type": "Standard"}, {"code": "B2 1AA", "area": "Birmingham", "type": "Standard"}]},
                        {"id": "UK_ENG_3", "name": "Liverpool", "postalCodes": [{"code": "L1 1AA", "area": "Liverpool City Centre", "type": "Standard"}, {"code": "L2 1AA", "area": "Liverpool", "type": "Standard"}]},
                        {"id": "UK_ENG_4", "name": "Leeds", "postalCodes": [{"code": "LS1 1AA", "area": "Leeds City Centre", "type": "Standard"}, {"code": "LS2 1AA", "area": "Leeds", "type": "Standard"}]},
                        {"id": "UK_ENG_5", "name": "Bristol", "postalCodes": [{"code": "BS1 1AA", "area": "Bristol City Centre", "type": "Standard"}, {"code": "BS2 1AA", "area": "Bristol", "type": "Standard"}]},
                        {"id": "UK_ENG_6", "name": "Sheffield", "postalCodes": [{"code": "S1 1AA", "area": "Sheffield City Centre", "type": "Standard"}, {"code": "S2 1AA", "area": "Sheffield", "type": "Standard"}]},
                        {"id": "UK_ENG_7", "name": "Newcastle", "postalCodes": [{"code": "NE1 1AA", "area": "Newcastle City Centre", "type": "Standard"}, {"code": "NE2 1AA", "area": "Newcastle", "type": "Standard"}]},
                        {"id": "UK_ENG_8", "name": "Nottingham", "postalCodes": [{"code": "NG1 1AA", "area": "Nottingham City Centre", "type": "Standard"}, {"code": "NG2 1AA", "area": "Nottingham", "type": "Standard"}]},
                        {"id": "UK_ENG_9", "name": "Leicester", "postalCodes": [{"code": "LE1 1AA", "area": "Leicester City Centre", "type": "Standard"}, {"code": "LE2 1AA", "area": "Leicester", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SCT",
                    "name": "Scotland",
                    "cities": [
                        {"id": "UK_SCT_0", "name": "Edinburgh", "postalCodes": [{"code": "EH1 1AA", "area": "Edinburgh City Centre", "type": "Standard"}, {"code": "EH2 1AA", "area": "Edinburgh", "type": "Standard"}]},
                        {"id": "UK_SCT_1", "name": "Glasgow", "postalCodes": [{"code": "G1 1AA", "area": "Glasgow City Centre", "type": "Standard"}, {"code": "G2 1AA", "area": "Glasgow", "type": "Standard"}]},
                        {"id": "UK_SCT_2", "name": "Aberdeen", "postalCodes": [{"code": "AB10 1AA", "area": "Aberdeen City Centre", "type": "Standard"}, {"code": "AB11 1AA", "area": "Aberdeen", "type": "Standard"}]},
                        {"id": "UK_SCT_3", "name": "Dundee", "postalCodes": [{"code": "DD1 1AA", "area": "Dundee City Centre", "type": "Standard"}, {"code": "DD2 1AA", "area": "Dundee", "type": "Standard"}]},
                        {"id": "UK_SCT_4", "name": "Inverness", "postalCodes": [{"code": "IV1 1AA", "area": "Inverness City Centre", "type": "Standard"}, {"code": "IV2 1AA", "area": "Inverness", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "WLS",
                    "name": "Wales",
                    "cities": [
                        {"id": "UK_WLS_0", "name": "Cardiff", "postalCodes": [{"code": "CF10 1AA", "area": "Cardiff City Centre", "type": "Standard"}, {"code": "CF11 1AA", "area": "Cardiff", "type": "Standard"}]},
                        {"id": "UK_WLS_1", "name": "Swansea", "postalCodes": [{"code": "SA1 1AA", "area": "Swansea City Centre", "type": "Standard"}, {"code": "SA2 1AA", "area": "Swansea", "type": "Standard"}]},
                        {"id": "UK_WLS_2", "name": "Newport", "postalCodes": [{"code": "NP10 1AA", "area": "Newport", "type": "Standard"}, {"code": "NP20 1AA", "area": "Newport City Centre", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "NIR",
                    "name": "Northern Ireland",
                    "cities": [
                        {"id": "UK_NIR_0", "name": "Belfast", "postalCodes": [{"code": "BT1 1AA", "area": "Belfast City Centre", "type": "Standard"}, {"code": "BT2 1AA", "area": "Belfast", "type": "Standard"}]},
                        {"id": "UK_NIR_1", "name": "Derry", "postalCodes": [{"code": "BT47 1AA", "area": "Derry", "type": "Standard"}, {"code": "BT48 1AA", "area": "Derry", "type": "Standard"}]},
                        {"id": "UK_NIR_2", "name": "Lisburn", "postalCodes": [{"code": "BT27 1AA", "area": "Lisburn", "type": "Standard"}, {"code": "BT28 1AA", "area": "Lisburn", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "CN",
            "name": "China",
            "states": [
                {
                    "id": "BJ",
                    "name": "Beijing",
                    "cities": [
                        {"id": "CN_BJ_0", "name": "Beijing", "postalCodes": [{"code": "100000", "area": "Beijing", "type": "Standard"}, {"code": "100001", "area": "Dongcheng", "type": "Standard"}, {"code": "100032", "area": "Xicheng", "type": "Standard"}]},
                        {"id": "CN_BJ_1", "name": "Chaoyang", "postalCodes": [{"code": "100020", "area": "Chaoyang District", "type": "Standard"}, {"code": "100026", "area": "Chaoyang", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SH",
                    "name": "Shanghai",
                    "cities": [
                        {"id": "CN_SH_0", "name": "Shanghai", "postalCodes": [{"code": "200000", "area": "Shanghai", "type": "Standard"}, {"code": "200001", "area": "Huangpu", "type": "Standard"}, {"code": "200030", "area": "Xuhui", "type": "Standard"}]},
                        {"id": "CN_SH_1", "name": "Pudong", "postalCodes": [{"code": "200120", "area": "Pudong New Area", "type": "Standard"}, {"code": "200135", "area": "Pudong", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "GD",
                    "name": "Guangdong",
                    "cities": [
                        {"id": "CN_GD_0", "name": "Guangzhou", "postalCodes": [{"code": "510000", "area": "Guangzhou", "type": "Standard"}, {"code": "510030", "area": "Yuexiu", "type": "Standard"}, {"code": "510620", "area": "Tianhe", "type": "Standard"}]},
                        {"id": "CN_GD_1", "name": "Shenzhen", "postalCodes": [{"code": "518000", "area": "Shenzhen", "type": "Standard"}, {"code": "518033", "area": "Futian", "type": "Standard"}, {"code": "518052", "area": "Nanshan", "type": "Standard"}]},
                        {"id": "CN_GD_2", "name": "Dongguan", "postalCodes": [{"code": "523000", "area": "Dongguan", "type": "Standard"}, {"code": "523808", "area": "Dongguan", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "ZJ",
                    "name": "Zhejiang",
                    "cities": [
                        {"id": "CN_ZJ_0", "name": "Hangzhou", "postalCodes": [{"code": "310000", "area": "Hangzhou", "type": "Standard"}, {"code": "310006", "area": "Shangcheng", "type": "Standard"}, {"code": "310013", "area": "Xihu", "type": "Standard"}]},
                        {"id": "CN_ZJ_1", "name": "Ningbo", "postalCodes": [{"code": "315000", "area": "Ningbo", "type": "Standard"}, {"code": "315040", "area": "Ningbo", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "JS",
                    "name": "Jiangsu",
                    "cities": [
                        {"id": "CN_JS_0", "name": "Nanjing", "postalCodes": [{"code": "210000", "area": "Nanjing", "type": "Standard"}, {"code": "210008", "area": "Xuanwu", "type": "Standard"}, {"code": "210009", "area": "Gulou", "type": "Standard"}]},
                        {"id": "CN_JS_1", "name": "Suzhou", "postalCodes": [{"code": "215000", "area": "Suzhou", "type": "Standard"}, {"code": "215004", "area": "Suzhou", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SC",
                    "name": "Sichuan",
                    "cities": [
                        {"id": "CN_SC_0", "name": "Chengdu", "postalCodes": [{"code": "610000", "area": "Chengdu", "type": "Standard"}, {"code": "610016", "area": "Jinjiang", "type": "Standard"}, {"code": "610031", "area": "Qingyang", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "HB",
                    "name": "Hubei",
                    "cities": [
                        {"id": "CN_HB_0", "name": "Wuhan", "postalCodes": [{"code": "430000", "area": "Wuhan", "type": "Standard"}, {"code": "430014", "area": "Jiang'an", "type": "Standard"}, {"code": "430060", "area": "Hanyang", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SN",
                    "name": "Shaanxi",
                    "cities": [
                        {"id": "CN_SN_0", "name": "Xi'an", "postalCodes": [{"code": "710000", "area": "Xi'an", "type": "Standard"}, {"code": "710001", "area": "Lianhu", "type": "Standard"}, {"code": "710068", "area": "Yanta", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "ID",
            "name": "Indonesia",
            "states": [
                {
                    "id": "JK",
                    "name": "Jakarta",
                    "cities": [
                        {"id": "ID_JK_0", "name": "Central Jakarta", "postalCodes": [{"code": "10110", "area": "Central Jakarta", "type": "Standard"}, {"code": "10120", "area": "Central Jakarta", "type": "Standard"}]},
                        {"id": "ID_JK_1", "name": "South Jakarta", "postalCodes": [{"code": "12110", "area": "South Jakarta", "type": "Standard"}, {"code": "12210", "area": "South Jakarta", "type": "Standard"}]},
                        {"id": "ID_JK_2", "name": "West Jakarta", "postalCodes": [{"code": "11110", "area": "West Jakarta", "type": "Standard"}, {"code": "11210", "area": "West Jakarta", "type": "Standard"}]},
                        {"id": "ID_JK_3", "name": "East Jakarta", "postalCodes": [{"code": "13110", "area": "East Jakarta", "type": "Standard"}, {"code": "13210", "area": "East Jakarta", "type": "Standard"}]},
                        {"id": "ID_JK_4", "name": "North Jakarta", "postalCodes": [{"code": "14110", "area": "North Jakarta", "type": "Standard"}, {"code": "14210", "area": "North Jakarta", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "BA",
                    "name": "Bali",
                    "cities": [
                        {"id": "ID_BA_0", "name": "Denpasar", "postalCodes": [{"code": "80111", "area": "Denpasar", "type": "Standard"}, {"code": "80112", "area": "Denpasar", "type": "Standard"}]},
                        {"id": "ID_BA_1", "name": "Kuta", "postalCodes": [{"code": "80361", "area": "Kuta", "type": "Standard"}, {"code": "80362", "area": "Kuta", "type": "Standard"}]},
                        {"id": "ID_BA_2", "name": "Ubud", "postalCodes": [{"code": "80571", "area": "Ubud", "type": "Standard"}, {"code": "80572", "area": "Ubud", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "JB",
                    "name": "West Java",
                    "cities": [
                        {"id": "ID_JB_0", "name": "Bandung", "postalCodes": [{"code": "40111", "area": "Bandung", "type": "Standard"}, {"code": "40112", "area": "Bandung", "type": "Standard"}]},
                        {"id": "ID_JB_1", "name": "Bekasi", "postalCodes": [{"code": "17111", "area": "Bekasi", "type": "Standard"}, {"code": "17112", "area": "Bekasi", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "JT",
                    "name": "Central Java",
                    "cities": [
                        {"id": "ID_JT_0", "name": "Semarang", "postalCodes": [{"code": "50111", "area": "Semarang", "type": "Standard"}, {"code": "50112", "area": "Semarang", "type": "Standard"}]},
                        {"id": "ID_JT_1", "name": "Surakarta", "postalCodes": [{"code": "57111", "area": "Surakarta", "type": "Standard"}, {"code": "57112", "area": "Surakarta", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "JI",
                    "name": "East Java",
                    "cities": [
                        {"id": "ID_JI_0", "name": "Surabaya", "postalCodes": [{"code": "60111", "area": "Surabaya", "type": "Standard"}, {"code": "60112", "area": "Surabaya", "type": "Standard"}]},
                        {"id": "ID_JI_1", "name": "Malang", "postalCodes": [{"code": "65111", "area": "Malang", "type": "Standard"}, {"code": "65112", "area": "Malang", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SU",
                    "name": "North Sumatra",
                    "cities": [
                        {"id": "ID_SU_0", "name": "Medan", "postalCodes": [{"code": "20111", "area": "Medan", "type": "Standard"}, {"code": "20112", "area": "Medan", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SS",
                    "name": "South Sulawesi",
                    "cities": [
                        {"id": "ID_SS_0", "name": "Makassar", "postalCodes": [{"code": "90111", "area": "Makassar", "type": "Standard"}, {"code": "90112", "area": "Makassar", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "GR",
            "name": "Greece",
            "states": [
                {
                    "id": "I",
                    "name": "Attica",
                    "cities": [
                        {"id": "GR_I_0", "name": "Athens", "postalCodes": [{"code": "10431", "area": "Athens", "type": "Standard"}, {"code": "10551", "area": "Athens", "type": "Standard"}, {"code": "10672", "area": "Athens", "type": "Standard"}]},
                        {"id": "GR_I_1", "name": "Piraeus", "postalCodes": [{"code": "18531", "area": "Piraeus", "type": "Standard"}, {"code": "18532", "area": "Piraeus", "type": "Standard"}]},
                        {"id": "GR_I_2", "name": "Kallithea", "postalCodes": [{"code": "17672", "area": "Kallithea", "type": "Standard"}, {"code": "17673", "area": "Kallithea", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "B",
                    "name": "Central Macedonia",
                    "cities": [
                        {"id": "GR_B_0", "name": "Thessaloniki", "postalCodes": [{"code": "54621", "area": "Thessaloniki", "type": "Standard"}, {"code": "54622", "area": "Thessaloniki", "type": "Standard"}, {"code": "54623", "area": "Thessaloniki", "type": "Standard"}]},
                        {"id": "GR_B_1", "name": "Serres", "postalCodes": [{"code": "62100", "area": "Serres", "type": "Standard"}, {"code": "62125", "area": "Serres", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "C",
                    "name": "West Greece",
                    "cities": [
                        {"id": "GR_C_0", "name": "Patras", "postalCodes": [{"code": "26221", "area": "Patras", "type": "Standard"}, {"code": "26222", "area": "Patras", "type": "Standard"}, {"code": "26223", "area": "Patras", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "D",
                    "name": "Epirus",
                    "cities": [
                        {"id": "GR_D_0", "name": "Ioannina", "postalCodes": [{"code": "45221", "area": "Ioannina", "type": "Standard"}, {"code": "45332", "area": "Ioannina", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "F",
                    "name": "Ionian Islands",
                    "cities": [
                        {"id": "GR_F_0", "name": "Corfu", "postalCodes": [{"code": "49100", "area": "Corfu", "type": "Standard"}, {"code": "49132", "area": "Corfu", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "H",
                    "name": "Crete",
                    "cities": [
                        {"id": "GR_H_0", "name": "Heraklion", "postalCodes": [{"code": "71201", "area": "Heraklion", "type": "Standard"}, {"code": "71202", "area": "Heraklion", "type": "Standard"}, {"code": "71414", "area": "Heraklion", "type": "Standard"}]},
                        {"id": "GR_H_1", "name": "Chania", "postalCodes": [{"code": "73131", "area": "Chania", "type": "Standard"}, {"code": "73132", "area": "Chania", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "SG",
            "name": "Singapore",
            "states": [
                {
                    "id": "SG",
                    "name": "Singapore",
                    "cities": [
                        {"id": "SG_SG_0", "name": "Singapore", "postalCodes": [{"code": "018956", "area": "Marina Bay", "type": "Standard"}, {"code": "019907", "area": "Raffles Place", "type": "Standard"}, {"code": "048424", "area": "Tanjong Pagar", "type": "Standard"}]},
                        {"id": "SG_SG_1", "name": "Jurong", "postalCodes": [{"code": "609601", "area": "Jurong East", "type": "Standard"}, {"code": "640649", "area": "Jurong West", "type": "Standard"}]},
                        {"id": "SG_SG_2", "name": "Tampines", "postalCodes": [{"code": "529510", "area": "Tampines", "type": "Standard"}, {"code": "520301", "area": "Tampines", "type": "Standard"}]},
                        {"id": "SG_SG_3", "name": "Woodlands", "postalCodes": [{"code": "730001", "area": "Woodlands", "type": "Standard"}, {"code": "738600", "area": "Woodlands", "type": "Standard"}]},
                        {"id": "SG_SG_4", "name": "Orchard", "postalCodes": [{"code": "238863", "area": "Orchard Road", "type": "Standard"}, {"code": "238801", "area": "Orchard", "type": "Standard"}]},
                        {"id": "SG_SG_5", "name": "Changi", "postalCodes": [{"code": "819642", "area": "Changi Airport", "type": "Standard"}, {"code": "507009", "area": "Changi", "type": "Standard"}]},
                        {"id": "SG_SG_6", "name": "Sentosa", "postalCodes": [{"code": "098375", "area": "Sentosa", "type": "Standard"}, {"code": "098382", "area": "Sentosa Cove", "type": "Standard"}]},
                        {"id": "SG_SG_7", "name": "Bedok", "postalCodes": [{"code": "460001", "area": "Bedok", "type": "Standard"}, {"code": "469001", "area": "Bedok", "type": "Standard"}]},
                        {"id": "SG_SG_8", "name": "Ang Mo Kio", "postalCodes": [{"code": "560001", "area": "Ang Mo Kio", "type": "Standard"}, {"code": "569933", "area": "Ang Mo Kio", "type": "Standard"}]},
                        {"id": "SG_SG_9", "name": "Clementi", "postalCodes": [{"code": "120001", "area": "Clementi", "type": "Standard"}, {"code": "129588", "area": "Clementi", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "TH",
            "name": "Thailand",
            "states": [
                {
                    "id": "BKK",
                    "name": "Bangkok",
                    "cities": [
                        {"id": "TH_BKK_0", "name": "Bangkok", "postalCodes": [{"code": "10100", "area": "Bangkok", "type": "Standard"}, {"code": "10200", "area": "Bangkok", "type": "Standard"}, {"code": "10300", "area": "Bangkok", "type": "Standard"}]},
                        {"id": "TH_BKK_1", "name": "Sathon", "postalCodes": [{"code": "10120", "area": "Sathon", "type": "Standard"}, {"code": "10121", "area": "Sathon", "type": "Standard"}]},
                        {"id": "TH_BKK_2", "name": "Sukhumvit", "postalCodes": [{"code": "10110", "area": "Sukhumvit", "type": "Standard"}, {"code": "10111", "area": "Sukhumvit", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "CM",
                    "name": "Chiang Mai",
                    "cities": [
                        {"id": "TH_CM_0", "name": "Chiang Mai", "postalCodes": [{"code": "50000", "area": "Chiang Mai", "type": "Standard"}, {"code": "50100", "area": "Chiang Mai", "type": "Standard"}, {"code": "50200", "area": "Chiang Mai", "type": "Standard"}]},
                        {"id": "TH_CM_1", "name": "Chiang Rai", "postalCodes": [{"code": "57000", "area": "Chiang Rai", "type": "Standard"}, {"code": "57100", "area": "Chiang Rai", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "PH",
                    "name": "Phuket",
                    "cities": [
                        {"id": "TH_PH_0", "name": "Phuket", "postalCodes": [{"code": "83000", "area": "Phuket", "type": "Standard"}, {"code": "83100", "area": "Phuket", "type": "Standard"}, {"code": "83110", "area": "Patong", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "CP",
                    "name": "Chonburi",
                    "cities": [
                        {"id": "TH_CP_0", "name": "Pattaya", "postalCodes": [{"code": "20150", "area": "Pattaya", "type": "Standard"}, {"code": "20260", "area": "Pattaya", "type": "Standard"}]},
                        {"id": "TH_CP_1", "name": "Chonburi", "postalCodes": [{"code": "20000", "area": "Chonburi", "type": "Standard"}, {"code": "20130", "area": "Chonburi", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SM",
                    "name": "Samut Prakan",
                    "cities": [
                        {"id": "TH_SM_0", "name": "Samut Prakan", "postalCodes": [{"code": "10270", "area": "Samut Prakan", "type": "Standard"}, {"code": "10280", "area": "Samut Prakan", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "NS",
                    "name": "Nakhon Si Thammarat",
                    "cities": [
                        {"id": "TH_NS_0", "name": "Nakhon Si Thammarat", "postalCodes": [{"code": "80000", "area": "Nakhon Si Thammarat", "type": "Standard"}, {"code": "80110", "area": "Nakhon Si Thammarat", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "KB",
                    "name": "Khon Kaen",
                    "cities": [
                        {"id": "TH_KB_0", "name": "Khon Kaen", "postalCodes": [{"code": "40000", "area": "Khon Kaen", "type": "Standard"}, {"code": "40001", "area": "Khon Kaen", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "MY",
            "name": "Malaysia",
            "states": [
                {
                    "id": "KL",
                    "name": "Kuala Lumpur",
                    "cities": [
                        {"id": "MY_KL_0", "name": "Kuala Lumpur", "postalCodes": [{"code": "50000", "area": "Kuala Lumpur", "type": "Standard"}, {"code": "50100", "area": "Kuala Lumpur", "type": "Standard"}, {"code": "50200", "area": "Kuala Lumpur", "type": "Standard"}]},
                        {"id": "MY_KL_1", "name": "Bukit Bintang", "postalCodes": [{"code": "55100", "area": "Bukit Bintang", "type": "Standard"}, {"code": "55101", "area": "Bukit Bintang", "type": "Standard"}]},
                        {"id": "MY_KL_2", "name": "KLCC", "postalCodes": [{"code": "50088", "area": "KLCC", "type": "Standard"}, {"code": "50050", "area": "KLCC", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "PJ",
                    "name": "Selangor",
                    "cities": [
                        {"id": "MY_PJ_0", "name": "Petaling Jaya", "postalCodes": [{"code": "46100", "area": "Petaling Jaya", "type": "Standard"}, {"code": "46200", "area": "Petaling Jaya", "type": "Standard"}, {"code": "46300", "area": "Petaling Jaya", "type": "Standard"}]},
                        {"id": "MY_PJ_1", "name": "Shah Alam", "postalCodes": [{"code": "40000", "area": "Shah Alam", "type": "Standard"}, {"code": "40100", "area": "Shah Alam", "type": "Standard"}]},
                        {"id": "MY_PJ_2", "name": "Subang Jaya", "postalCodes": [{"code": "47500", "area": "Subang Jaya", "type": "Standard"}, {"code": "47600", "area": "Subang Jaya", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "PG",
                    "name": "Penang",
                    "cities": [
                        {"id": "MY_PG_0", "name": "George Town", "postalCodes": [{"code": "10000", "area": "George Town", "type": "Standard"}, {"code": "10100", "area": "George Town", "type": "Standard"}, {"code": "10200", "area": "George Town", "type": "Standard"}]},
                        {"id": "MY_PG_1", "name": "Bayan Lepas", "postalCodes": [{"code": "11900", "area": "Bayan Lepas", "type": "Standard"}, {"code": "11950", "area": "Bayan Lepas", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "JH",
                    "name": "Johor",
                    "cities": [
                        {"id": "MY_JH_0", "name": "Johor Bahru", "postalCodes": [{"code": "80000", "area": "Johor Bahru", "type": "Standard"}, {"code": "80100", "area": "Johor Bahru", "type": "Standard"}, {"code": "80200", "area": "Johor Bahru", "type": "Standard"}]},
                        {"id": "MY_JH_1", "name": "Iskandar Puteri", "postalCodes": [{"code": "79000", "area": "Iskandar Puteri", "type": "Standard"}, {"code": "79100", "area": "Iskandar Puteri", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "ML",
                    "name": "Malacca",
                    "cities": [
                        {"id": "MY_ML_0", "name": "Malacca City", "postalCodes": [{"code": "75000", "area": "Malacca City", "type": "Standard"}, {"code": "75100", "area": "Malacca City", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SA",
                    "name": "Sabah",
                    "cities": [
                        {"id": "MY_SA_0", "name": "Kota Kinabalu", "postalCodes": [{"code": "88000", "area": "Kota Kinabalu", "type": "Standard"}, {"code": "88100", "area": "Kota Kinabalu", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SR",
                    "name": "Sarawak",
                    "cities": [
                        {"id": "MY_SR_0", "name": "Kuching", "postalCodes": [{"code": "93000", "area": "Kuching", "type": "Standard"}, {"code": "93100", "area": "Kuching", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "PH",
            "name": "Philippines",
            "states": [
                {
                    "id": "NCR",
                    "name": "Metro Manila",
                    "cities": [
                        {"id": "PH_NCR_0", "name": "Manila", "postalCodes": [{"code": "1000", "area": "Manila", "type": "Standard"}, {"code": "1001", "area": "Manila", "type": "Standard"}, {"code": "1002", "area": "Manila", "type": "Standard"}]},
                        {"id": "PH_NCR_1", "name": "Makati", "postalCodes": [{"code": "1200", "area": "Makati", "type": "Standard"}, {"code": "1210", "area": "Makati", "type": "Standard"}, {"code": "1220", "area": "Makati", "type": "Standard"}]},
                        {"id": "PH_NCR_2", "name": "Quezon City", "postalCodes": [{"code": "1100", "area": "Quezon City", "type": "Standard"}, {"code": "1101", "area": "Quezon City", "type": "Standard"}, {"code": "1102", "area": "Quezon City", "type": "Standard"}]},
                        {"id": "PH_NCR_3", "name": "Taguig", "postalCodes": [{"code": "1630", "area": "Taguig", "type": "Standard"}, {"code": "1631", "area": "Taguig", "type": "Standard"}, {"code": "1632", "area": "Taguig", "type": "Standard"}]},
                        {"id": "PH_NCR_4", "name": "Pasig", "postalCodes": [{"code": "1600", "area": "Pasig", "type": "Standard"}, {"code": "1601", "area": "Pasig", "type": "Standard"}, {"code": "1602", "area": "Pasig", "type": "Standard"}]},
                        {"id": "PH_NCR_5", "name": "Mandaluyong", "postalCodes": [{"code": "1550", "area": "Mandaluyong", "type": "Standard"}, {"code": "1551", "area": "Mandaluyong", "type": "Standard"}, {"code": "1552", "area": "Mandaluyong", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "CEB",
                    "name": "Cebu",
                    "cities": [
                        {"id": "PH_CEB_0", "name": "Cebu City", "postalCodes": [{"code": "6000", "area": "Cebu City", "type": "Standard"}, {"code": "6010", "area": "Cebu City", "type": "Standard"}, {"code": "6020", "area": "Cebu City", "type": "Standard"}]},
                        {"id": "PH_CEB_1", "name": "Mandaue", "postalCodes": [{"code": "6014", "area": "Mandaue", "type": "Standard"}, {"code": "6015", "area": "Mandaue", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "DAV",
                    "name": "Davao del Sur",
                    "cities": [
                        {"id": "PH_DAV_0", "name": "Davao City", "postalCodes": [{"code": "8000", "area": "Davao City", "type": "Standard"}, {"code": "8010", "area": "Davao City", "type": "Standard"}, {"code": "8020", "area": "Davao City", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "LAG",
                    "name": "Laguna",
                    "cities": [
                        {"id": "PH_LAG_0", "name": "Calamba", "postalCodes": [{"code": "4027", "area": "Calamba", "type": "Standard"}, {"code": "4028", "area": "Calamba", "type": "Standard"}]},
                        {"id": "PH_LAG_1", "name": "Santa Rosa", "postalCodes": [{"code": "4026", "area": "Santa Rosa", "type": "Standard"}, {"code": "4025", "area": "Santa Rosa", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "BTG",
                    "name": "Batangas",
                    "cities": [
                        {"id": "PH_BTG_0", "name": "Batangas City", "postalCodes": [{"code": "4200", "area": "Batangas City", "type": "Standard"}, {"code": "4210", "area": "Batangas City", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "PAM",
                    "name": "Pampanga",
                    "cities": [
                        {"id": "PH_PAM_0", "name": "Angeles City", "postalCodes": [{"code": "2009", "area": "Angeles City", "type": "Standard"}, {"code": "2010", "area": "Angeles City", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "ILO",
                    "name": "Iloilo",
                    "cities": [
                        {"id": "PH_ILO_0", "name": "Iloilo City", "postalCodes": [{"code": "5000", "area": "Iloilo City", "type": "Standard"}, {"code": "5010", "area": "Iloilo City", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "KR",
            "name": "South Korea",
            "states": [
                {
                    "id": "SEO",
                    "name": "Seoul",
                    "cities": [
                        {"id": "KR_SEO_0", "name": "Seoul", "postalCodes": [{"code": "01000", "area": "Seoul", "type": "Standard"}, {"code": "01100", "area": "Seoul", "type": "Standard"}, {"code": "01200", "area": "Seoul", "type": "Standard"}]},
                        {"id": "KR_SEO_1", "name": "Gangnam", "postalCodes": [{"code": "06000", "area": "Gangnam", "type": "Standard"}, {"code": "06100", "area": "Gangnam", "type": "Standard"}, {"code": "06200", "area": "Gangnam", "type": "Standard"}]},
                        {"id": "KR_SEO_2", "name": "Jongno", "postalCodes": [{"code": "03000", "area": "Jongno", "type": "Standard"}, {"code": "03100", "area": "Jongno", "type": "Standard"}]},
                        {"id": "KR_SEO_3", "name": "Mapo", "postalCodes": [{"code": "03900", "area": "Mapo", "type": "Standard"}, {"code": "04000", "area": "Mapo", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "BUS",
                    "name": "Busan",
                    "cities": [
                        {"id": "KR_BUS_0", "name": "Busan", "postalCodes": [{"code": "46000", "area": "Busan", "type": "Standard"}, {"code": "46100", "area": "Busan", "type": "Standard"}, {"code": "46200", "area": "Busan", "type": "Standard"}]},
                        {"id": "KR_BUS_1", "name": "Haeundae", "postalCodes": [{"code": "48000", "area": "Haeundae", "type": "Standard"}, {"code": "48100", "area": "Haeundae", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "ICN",
                    "name": "Incheon",
                    "cities": [
                        {"id": "KR_ICN_0", "name": "Incheon", "postalCodes": [{"code": "21000", "area": "Incheon", "type": "Standard"}, {"code": "21100", "area": "Incheon", "type": "Standard"}, {"code": "21200", "area": "Incheon", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "DG",
                    "name": "Daegu",
                    "cities": [
                        {"id": "KR_DG_0", "name": "Daegu", "postalCodes": [{"code": "41000", "area": "Daegu", "type": "Standard"}, {"code": "41100", "area": "Daegu", "type": "Standard"}, {"code": "41200", "area": "Daegu", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "GJ",
                    "name": "Gwangju",
                    "cities": [
                        {"id": "KR_GJ_0", "name": "Gwangju", "postalCodes": [{"code": "61000", "area": "Gwangju", "type": "Standard"}, {"code": "61100", "area": "Gwangju", "type": "Standard"}, {"code": "61200", "area": "Gwangju", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "DJ",
                    "name": "Daejeon",
                    "cities": [
                        {"id": "KR_DJ_0", "name": "Daejeon", "postalCodes": [{"code": "34000", "area": "Daejeon", "type": "Standard"}, {"code": "34100", "area": "Daejeon", "type": "Standard"}, {"code": "34200", "area": "Daejeon", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "ULS",
                    "name": "Ulsan",
                    "cities": [
                        {"id": "KR_ULS_0", "name": "Ulsan", "postalCodes": [{"code": "44000", "area": "Ulsan", "type": "Standard"}, {"code": "44100", "area": "Ulsan", "type": "Standard"}, {"code": "44200", "area": "Ulsan", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "GG",
                    "name": "Gyeonggi",
                    "cities": [
                        {"id": "KR_GG_0", "name": "Suwon", "postalCodes": [{"code": "16200", "area": "Suwon", "type": "Standard"}, {"code": "16300", "area": "Suwon", "type": "Standard"}, {"code": "16400", "area": "Suwon", "type": "Standard"}]},
                        {"id": "KR_GG_1", "name": "Goyang", "postalCodes": [{"code": "10200", "area": "Goyang", "type": "Standard"}, {"code": "10300", "area": "Goyang", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "AE",
            "name": "United Arab Emirates",
            "states": [
                {
                    "id": "DXB",
                    "name": "Dubai",
                    "cities": [
                        {"id": "AE_DXB_0", "name": "Dubai", "postalCodes": [{"code": "00000", "area": "Dubai", "type": "Standard"}, {"code": "12345", "area": "Downtown Dubai", "type": "Standard"}, {"code": "54321", "area": "Dubai Marina", "type": "Standard"}]},
                        {"id": "AE_DXB_1", "name": "Deira", "postalCodes": [{"code": "11111", "area": "Deira", "type": "Standard"}, {"code": "22222", "area": "Deira", "type": "Standard"}]},
                        {"id": "AE_DXB_2", "name": "Bur Dubai", "postalCodes": [{"code": "33333", "area": "Bur Dubai", "type": "Standard"}, {"code": "44444", "area": "Bur Dubai", "type": "Standard"}]},
                        {"id": "AE_DXB_3", "name": "Jumeirah", "postalCodes": [{"code": "55555", "area": "Jumeirah", "type": "Standard"}, {"code": "66666", "area": "Jumeirah", "type": "Standard"}]},
                        {"id": "AE_DXB_4", "name": "Business Bay", "postalCodes": [{"code": "77777", "area": "Business Bay", "type": "Standard"}, {"code": "88888", "area": "Business Bay", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "AUH",
                    "name": "Abu Dhabi",
                    "cities": [
                        {"id": "AE_AUH_0", "name": "Abu Dhabi", "postalCodes": [{"code": "00000", "area": "Abu Dhabi", "type": "Standard"}, {"code": "11111", "area": "Corniche", "type": "Standard"}, {"code": "22222", "area": "Al Reem Island", "type": "Standard"}]},
                        {"id": "AE_AUH_1", "name": "Al Ain", "postalCodes": [{"code": "33333", "area": "Al Ain", "type": "Standard"}, {"code": "44444", "area": "Al Ain", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SHJ",
                    "name": "Sharjah",
                    "cities": [
                        {"id": "AE_SHJ_0", "name": "Sharjah", "postalCodes": [{"code": "00000", "area": "Sharjah", "type": "Standard"}, {"code": "11111", "area": "Sharjah", "type": "Standard"}, {"code": "22222", "area": "Sharjah", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "AJM",
                    "name": "Ajman",
                    "cities": [
                        {"id": "AE_AJM_0", "name": "Ajman", "postalCodes": [{"code": "00000", "area": "Ajman", "type": "Standard"}, {"code": "11111", "area": "Ajman", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "RAK",
                    "name": "Ras Al Khaimah",
                    "cities": [
                        {"id": "AE_RAK_0", "name": "Ras Al Khaimah", "postalCodes": [{"code": "00000", "area": "Ras Al Khaimah", "type": "Standard"}, {"code": "11111", "area": "Ras Al Khaimah", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "FUJ",
                    "name": "Fujairah",
                    "cities": [
                        {"id": "AE_FUJ_0", "name": "Fujairah", "postalCodes": [{"code": "00000", "area": "Fujairah", "type": "Standard"}, {"code": "11111", "area": "Fujairah", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "UAQ",
                    "name": "Umm Al Quwain",
                    "cities": [
                        {"id": "AE_UAQ_0", "name": "Umm Al Quwain", "postalCodes": [{"code": "00000", "area": "Umm Al Quwain", "type": "Standard"}, {"code": "11111", "area": "Umm Al Quwain", "type": "Standard"}]}
                    ]
                }
            ]
        },
        {
            "id": "IL",
            "name": "Israel",
            "states": [
                {
                    "id": "TA",
                    "name": "Tel Aviv District",
                    "cities": [
                        {"id": "IL_TA_0", "name": "Tel Aviv", "postalCodes": [{"code": "6100000", "area": "Tel Aviv", "type": "Standard"}, {"code": "6100001", "area": "Tel Aviv", "type": "Standard"}, {"code": "6100002", "area": "Tel Aviv", "type": "Standard"}]},
                        {"id": "IL_TA_1", "name": "Ramat Gan", "postalCodes": [{"code": "5200000", "area": "Ramat Gan", "type": "Standard"}, {"code": "5200001", "area": "Ramat Gan", "type": "Standard"}]},
                        {"id": "IL_TA_2", "name": "Givatayim", "postalCodes": [{"code": "5300000", "area": "Givatayim", "type": "Standard"}, {"code": "5300001", "area": "Givatayim", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "JM",
                    "name": "Jerusalem District",
                    "cities": [
                        {"id": "IL_JM_0", "name": "Jerusalem", "postalCodes": [{"code": "9100000", "area": "Jerusalem", "type": "Standard"}, {"code": "9100001", "area": "Jerusalem", "type": "Standard"}, {"code": "9100002", "area": "Jerusalem", "type": "Standard"}]},
                        {"id": "IL_JM_1", "name": "Bet Shemesh", "postalCodes": [{"code": "9900000", "area": "Bet Shemesh", "type": "Standard"}, {"code": "9900001", "area": "Bet Shemesh", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "HA",
                    "name": "Haifa District",
                    "cities": [
                        {"id": "IL_HA_0", "name": "Haifa", "postalCodes": [{"code": "3300000", "area": "Haifa", "type": "Standard"}, {"code": "3300001", "area": "Haifa", "type": "Standard"}, {"code": "3300002", "area": "Haifa", "type": "Standard"}]},
                        {"id": "IL_HA_1", "name": "Hadera", "postalCodes": [{"code": "3800000", "area": "Hadera", "type": "Standard"}, {"code": "3800001", "area": "Hadera", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "CEN",
                    "name": "Central District",
                    "cities": [
                        {"id": "IL_CEN_0", "name": "Petah Tikva", "postalCodes": [{"code": "4900000", "area": "Petah Tikva", "type": "Standard"}, {"code": "4900001", "area": "Petah Tikva", "type": "Standard"}, {"code": "4900002", "area": "Petah Tikva", "type": "Standard"}]},
                        {"id": "IL_CEN_1", "name": "Rishon LeZion", "postalCodes": [{"code": "7500000", "area": "Rishon LeZion", "type": "Standard"}, {"code": "7500001", "area": "Rishon LeZion", "type": "Standard"}]},
                        {"id": "IL_CEN_2", "name": "Netanya", "postalCodes": [{"code": "4200000", "area": "Netanya", "type": "Standard"}, {"code": "4200001", "area": "Netanya", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "SOUTH",
                    "name": "Southern District",
                    "cities": [
                        {"id": "IL_SOUTH_0", "name": "Beersheba", "postalCodes": [{"code": "8400000", "area": "Beersheba", "type": "Standard"}, {"code": "8400001", "area": "Beersheba", "type": "Standard"}, {"code": "8400002", "area": "Beersheba", "type": "Standard"}]},
                        {"id": "IL_SOUTH_1", "name": "Ashdod", "postalCodes": [{"code": "7700000", "area": "Ashdod", "type": "Standard"}, {"code": "7700001", "area": "Ashdod", "type": "Standard"}]},
                        {"id": "IL_SOUTH_2", "name": "Ashkelon", "postalCodes": [{"code": "7800000", "area": "Ashkelon", "type": "Standard"}, {"code": "7800001", "area": "Ashkelon", "type": "Standard"}]}
                    ]
                },
                {
                    "id": "NORTH",
                    "name": "Northern District",
                    "cities": [
                        {"id": "IL_NORTH_0", "name": "Nazareth", "postalCodes": [{"code": "1600000", "area": "Nazareth", "type": "Standard"}, {"code": "1600001", "area": "Nazareth", "type": "Standard"}]},
                        {"id": "IL_NORTH_1", "name": "Tiberias", "postalCodes": [{"code": "1410000", "area": "Tiberias", "type": "Standard"}, {"code": "1410001", "area": "Tiberias", "type": "Standard"}]}
                    ]
                }
            ]
        }
    ]
    
    # 添加缺失的国家
    added = []
    for country in missing_countries:
        if country['id'] not in existing_ids:
            data['countries'].append(country)
            added.append(country['id'])
    
    # 保存更新后的数据
    with open('postal_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已添加 {len(added)} 个国家: {', '.join(added)}")
    print(f"现在共有 {len(data['countries'])} 个国家")

if __name__ == '__main__':
    add_missing_countries()
