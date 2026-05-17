const fs = require('fs');
const path = require('path');

// Read mockData.js
const mockDataPath = path.join(__dirname, 'mockData.js');
const mockDataContent = fs.readFileSync(mockDataPath, 'utf8');

// Count cities for each country by finding country blocks
// Pattern: find each country entry and count cities within
const countryCityCounts = {};

// Find all country IDs first
const countryIdRegex = /\{\s*id:\s*"([A-Z_]+)",\s*name:\s*"([^"]+)"/g;
const countries = [];
let m;
while ((m = countryIdRegex.exec(mockDataContent)) !== null) {
    countries.push({ id: m[1], name: m[2], pos: m.index });
}

// For each country, count cities in its block
for (let i = 0; i < countries.length; i++) {
    const country = countries[i];
    const startPos = country.pos;
    const endPos = i < countries.length - 1 ? countries[i + 1].pos : mockDataContent.length;
    const block = mockDataContent.slice(startPos, endPos);

    // Count cities: each city has "postalCodes:" array
    const cityMatches = block.match(/postalCodes:\s*\[/g);
    const cityCount = cityMatches ? cityMatches.length : 0;
    countryCityCounts[country.id] = cityCount;
}

console.log('=== Country City Counts ===');
for (const [id, count] of Object.entries(countryCityCounts).sort()) {
    console.log(`${id}: ${count} cities`);
}

// Map country ID to HTML file slug
const idToSlug = {
    'US': 'us',
    'CA': 'canada',
    'GB': 'united-kingdom',
    'UK': 'united-kingdom',
    'DE': 'germany',
    'FR': 'france',
    'IT': 'italy',
    'ES': 'spain',
    'PT': 'portugal',
    'NL': 'netherlands',
    'BE': 'belgium',
    'CH': 'switzerland',
    'AT': 'austria',
    'SE': 'sweden',
    'NO': 'norway',
    'DK': 'denmark',
    'FI': 'finland',
    'PL': 'poland',
    'CZ': 'czech-republic',
    'SK': 'slovakia',
    'HU': 'hungary',
    'RO': 'romania',
    'BG': 'bulgaria',
    'HR': 'croatia',
    'SI': 'slovenia',
    'GR': 'greece',
    'IE': 'ireland',
    'AU': 'australia',
    'NZ': 'new-zealand',
    'JP': 'japan',
    'KR': 'south-korea',
    'CN': 'china',
    'IN': 'india',
    'BR': 'brazil',
    'MX': 'mexico',
    'AR': 'argentina',
    'CL': 'chile',
    'ZA': 'south-africa',
    'EG': 'egypt',
    'TR': 'turkey',
    'RU': 'russia',
    'UA': 'ukraine',
    'IL': 'israel',
    'AE': 'uae',
    'SG': 'singapore',
    'MY': 'malaysia',
    'TH': 'thailand',
    'PH': 'philippines',
    'ID': 'indonesia',
    'VN': 'vietnam',
    'PK': 'pakistan',
    'BD': 'bangladesh',
    'LK': 'sri-lanka',
    'NP': 'nepal',
    'SA': 'saudi-arabia',
    'KW': 'kuwait',
    'QA': 'qatar',
    'JO': 'jordan',
    'LB': 'lebanon',
    'OM': 'oman',
    'BH': 'bahrain',
    'IS': 'iceland',
    'MT': 'malta',
    'CY': 'cyprus',
    'LU': 'luxembourg',
    'LI': 'liechtenstein',
    'MC': 'monaco',
    'AD': 'andorra',
    'SM': 'san-marino',
    'VA': 'vatican-city',
    'EE': 'estonia',
    'LV': 'latvia',
    'LT': 'lithuania',
    'BY': 'belarus',
    'MD': 'moldova',
    'GE': 'georgia',
    'AM': 'armenia',
    'AZ': 'azerbaijan',
    'KZ': 'kazakhstan',
    'UZ': 'uzbekistan',
    'KG': 'kyrgyzstan',
    'TJ': 'tajikistan',
    'TM': 'turkmenistan',
    'MN': 'mongolia',
    'TW': 'taiwan',
    'HK': 'hong-kong',
    'MO': 'macau',
    'KH': 'cambodia',
    'LA': 'laos',
    'MM': 'myanmar',
    'BN': 'brunei',
    'PG': 'papua-new-guinea',
    'FJ': 'fiji',
    'SB': 'solomon-islands',
    'VU': 'vanuatu',
    'NC': 'new-caledonia',
    'PF': 'french-polynesia',
    'GU': 'guam',
    'AS': 'american-samoa',
    'KI': 'kiribati',
    'TV': 'tuvalu',
    'NR': 'nauru',
    'TO': 'tonga',
    'WS': 'samoa',
    'FM': 'micronesia',
    'MH': 'marshall-islands',
    'PW': 'palau',
    'CK': 'cook-islands',
    'NU': 'niue',
    'TK': 'tokelau',
    'WF': 'wallis-and-futuna',
    'PN': 'pitcairn',
    'IO': 'british-indian-ocean-territory',
    'CX': 'christmas-island',
    'CC': 'cocos-islands',
    'NF': 'norfolk-island',
    'YT': 'mayotte',
    'RE': 'reunion',
    'SC': 'seychelles',
    'MU': 'mauritius',
    'MV': 'maldives',
    'MG': 'madagascar',
    'KM': 'comoros',
    'DZ': 'algeria',
    'MA': 'morocco',
    'TN': 'tunisia',
    'LY': 'libya',
    'SD': 'sudan',
    'ET': 'ethiopia',
    'KE': 'kenya',
    'UG': 'uganda',
    'TZ': 'tanzania',
    'RW': 'rwanda',
    'BI': 'burundi',
    'MW': 'malawi',
    'MZ': 'mozambique',
    'ZM': 'zambia',
    'ZW': 'zimbabwe',
    'BW': 'botswana',
    'NA': 'namibia',
    'AO': 'angola',
    'CD': 'democratic-republic-of-congo',
    'CG': 'republic-of-congo',
    'GA': 'gabon',
    'GQ': 'equatorial-guinea',
    'ST': 'sao-tome-and-principe',
    'CM': 'cameroon',
    'CF': 'central-african-republic',
    'TD': 'chad',
    'NE': 'niger',
    'ML': 'mali',
    'BF': 'burkina-faso',
    'SN': 'senegal',
    'GM': 'gambia',
    'GW': 'guinea-bissau',
    'GN': 'guinea',
    'SL': 'sierra-leone',
    'LR': 'liberia',
    'CI': 'ivory-coast',
    'GH': 'ghana',
    'TG': 'togo',
    'BJ': 'benin',
    'NG': 'nigeria',
    'SH': 'saint-helena',
    'AC': 'ascension',
    'TA': 'tristan-da-cunha',
    'EH': 'western-sahara',
    'SO': 'somalia',
    'DJ': 'djibouti',
    'ER': 'eritrea',
    'SS': 'south-sudan',
    'MR': 'mauritania'
};

const slugToId = {};
for (const [id, slug] of Object.entries(idToSlug)) {
    if (!slugToId[slug]) {
        slugToId[slug] = id;
    }
}

// Find all HTML files
const htmlFiles = fs.readdirSync(__dirname).filter(f => f.endsWith('-postal-code.html'));
console.log(`\n=== Found ${htmlFiles.length} country HTML files ===`);

// Fix HTML files
let fixedCount = 0;
for (const file of htmlFiles) {
    const filePath = path.join(__dirname, file);
    let content = fs.readFileSync(filePath, 'utf8');
    const originalContent = content;

    // Extract slug from filename
    const slug = file.replace('-postal-code.html', '');
    const countryId = slugToId[slug];

    if (!countryId) {
        console.log(`Warning: No country ID mapping for ${file}`);
        continue;
    }

    const cityCount = countryCityCounts[countryId] || 0;

    // Fix "0+ cities" or any "X+ cities" in meta description
    // Pattern: "Search zip codes for N+ cities in CountryName"
    content = content.replace(
        /(content="Free [^"]+?\. Search zip codes for )\d+\+? cities( in [^"]+")/,
        `$1${cityCount}+ cities$2`
    );

    // Fix og:description and twitter:description
    content = content.replace(
        /(content="Search postal codes for )\d+\+? cities( in [^"]+")/g,
        `$1${cityCount}+ cities$2`
    );

    if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        fixedCount++;
        console.log(`Fixed ${file}: ${cityCount} cities`);
    } else {
        // Check if it still has 0+ cities
        if (content.includes('0+ cities')) {
            console.log(`STILL HAS 0+ cities: ${file}`);
        }
    }
}

console.log(`\n=== Fixed ${fixedCount} HTML files ===`);
