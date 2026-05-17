const fs = require('fs');

const filePath = 'mockData.js';
let content = fs.readFileSync(filePath, 'utf8');

// Extended postal code prefix to city mapping (covers all German postal codes)
const prefixToCity = {
  '01': 'Dresden', '02': 'Görlitz', '03': 'Cottbus', '04': 'Leipzig',
  '05': 'Chemnitz', '06': 'Halle', '07': 'Jena', '08': 'Zwickau',
  '09': 'Erfurt',
  '10': 'Berlin', '11': 'Berlin', '12': 'Berlin', '13': 'Berlin', '14': 'Berlin',
  '15': 'Berlin', '16': 'Berlin', '17': 'Berlin', '18': 'Berlin', '19': 'Berlin',
  '20': 'Hamburg', '21': 'Hamburg', '22': 'Hamburg', '23': 'Hamburg', '24': 'Hamburg',
  '25': 'Hamburg', '26': 'Bremen', '27': 'Bremen', '28': 'Bremen', '29': 'Bremen',
  '30': 'Hanover', '31': 'Hanover', '32': 'Hanover', '33': 'Hanover', '34': 'Hanover',
  '35': 'Hanover', '36': 'Hanover', '37': 'Hanover', '38': 'Hanover', '39': 'Hanover',
  '40': 'Düsseldorf', '41': 'Düsseldorf', '42': 'Düsseldorf', '43': 'Düsseldorf',
  '44': 'Dortmund', '45': 'Essen', '46': 'Oberhausen', '47': 'Duisburg',
  '48': 'Münster', '49': 'Osnabrück',
  '50': 'Cologne', '51': 'Cologne', '52': 'Cologne', '53': 'Cologne',
  '54': 'Trier', '55': 'Mainz', '56': 'Koblenz', '57': 'Siegen',
  '58': 'Hagen', '59': 'Bielefeld',
  '60': 'Frankfurt', '61': 'Frankfurt', '62': 'Frankfurt', '63': 'Frankfurt',
  '64': 'Darmstadt', '65': 'Wiesbaden', '66': 'Saarbrücken', '67': 'Kaiserslautern',
  '68': 'Mannheim', '69': 'Heidelberg',
  '70': 'Stuttgart', '71': 'Stuttgart', '72': 'Stuttgart', '73': 'Stuttgart',
  '74': 'Stuttgart', '75': 'Stuttgart', '76': 'Karlsruhe', '77': 'Freiburg',
  '78': 'Konstanz', '79': 'Freiburg',
  '80': 'Munich', '81': 'Munich', '82': 'Munich', '83': 'Munich', '84': 'Munich',
  '85': 'Munich', '86': 'Augsburg', '87': 'Würzburg', '88': 'Ravensburg',
  '89': 'Ulm',
  '90': 'Nuremberg', '91': 'Nuremberg', '92': 'Nuremberg', '93': 'Regensburg',
  '94': 'Passau', '95': 'Bayreuth', '96': 'Bamberg', '97': 'Würzburg',
  '98': 'Coburg', '99': 'Erfurt'
};

// Find Germany section
const germanyStart = content.indexOf('id: "DE"');
const germanyEnd = content.indexOf('id: "FR"');

if (germanyStart === -1 || germanyEnd === -1) {
  console.log('Could not find Germany section');
  process.exit(1);
}

let germanySection = content.substring(germanyStart, germanyEnd);
let replaceCount = 0;
let areaReplaceCount = 0;

// Match all city entries in Germany section
// Pattern: { id: "DE_X_X", name: "CURRENT_NAME", postalCodes: [{ code: "POSTAL_CODE", area: "AREA_NAME"
const cityPattern = /\{ id: "DE_\d+_\d+", name: "([^"]+)", postalCodes: \[\{ code: "(\d{5})", area: "([^"]+)"/g;

let match;
const replacements = [];

while ((match = cityPattern.exec(germanySection)) !== null) {
  const currentName = match[1];
  const postalCode = match[2];
  const currentArea = match[3];
  const prefix = postalCode.substring(0, 2);
  const newCityName = prefixToCity[prefix];

  if (newCityName) {
    // Replace name if it's a company name or different from expected
    if (currentName !== newCityName &&
        (currentName.includes('GmbH') || currentName.includes('AG') ||
         currentName.includes('KG') || currentName.includes('mbH') ||
         currentName.length > 25 || currentName.includes('Deutsche Post') ||
         currentName.includes('Universität') || currentName.includes('Agentur') ||
         currentName.includes('Finanzamt') || currentName.includes('Landes'))) {

      const oldStr = `name: "${currentName}", postalCodes: [{ code: "${postalCode}"`;
      const newStr = `name: "${newCityName}", postalCodes: [{ code: "${postalCode}"`;
      germanySection = germanySection.replace(oldStr, newStr);
      replaceCount++;
    }

    // Replace area if it's a company name or different from expected
    if (currentArea !== newCityName &&
        (currentArea.includes('GmbH') || currentArea.includes('AG') ||
         currentArea.includes('KG') || currentArea.includes('mbH') ||
         currentArea.length > 25 || currentArea.includes('Deutsche Post') ||
         currentArea.includes('Universität') || currentArea.includes('Agentur') ||
         currentArea.includes('Finanzamt') || currentArea.includes('Landes') ||
         currentArea.includes('Stadtwerke') || currentArea.includes('Sparkasse'))) {

      const oldAreaStr = `code: "${postalCode}", area: "${currentArea}"`;
      const newAreaStr = `code: "${postalCode}", area: "${newCityName}"`;
      germanySection = germanySection.replace(oldAreaStr, newAreaStr);
      areaReplaceCount++;
    }
  }
}

// Update content
content = content.substring(0, germanyStart) + germanySection + content.substring(germanyEnd);

// Write back
fs.writeFileSync(filePath, content, 'utf8');

console.log(`Replaced ${replaceCount} city names in Germany section`);
console.log(`Replaced ${areaReplaceCount} area names in Germany section`);
console.log('Germany data updated successfully');
