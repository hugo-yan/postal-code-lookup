const fs = require('fs');

const filePath = 'mockData.js';
let content = fs.readFileSync(filePath, 'utf8');

// Find Germany section
const germanyStart = content.indexOf('id: "DE"');
const germanyEnd = content.indexOf('id: "FR"');

if (germanyStart === -1 || germanyEnd === -1) {
  console.log('Could not find Germany section');
  process.exit(1);
}

let germanySection = content.substring(germanyStart, germanyEnd);
let replaceCount = 0;

// Match all city entries in Germany section
const cityPattern = /\{ id: "(DE_\d+_\d+)", name: "([^"]+)", postalCodes: \[([^\]]*)\] \}/g;

let match;
while ((match = cityPattern.exec(germanySection)) !== null) {
  const fullMatch = match[0];
  const cityId = match[1];
  const currentName = match[2];
  const postalCodesBlock = match[3];

  // Check if name contains company/institution keywords
  const isCompany = /GmbH|AG|KG|mbH|Deutsche Post|Universität|Agentur|Finanzamt|Landes|Stadtwerke|Sparkasse|Staatskanzlei|Aufbaubank|IHK|BKK|Rentenversicherung|Patentamt|Schwarzbierbrauerei|Bußgeldstelle|Stadtverwaltung|HUK-Coburg|AOK|Amtsgericht|Köstritzer|Mondelez|Familienkasse|Klinikum|Rundfunk|Bibliothek|Zeitung|Versicherung|Kasse|Werk|Bank|Brauerei/i.test(currentName);

  if (isCompany) {
    // Extract first postal code to determine city
    const codeMatch = postalCodesBlock.match(/code: "(\d{5})/);
    if (codeMatch) {
      const postalCode = codeMatch[1];
      const prefix = postalCode.substring(0, 2);

      // Map prefix to city
      const prefixToCity = {
        '01': 'Dresden', '02': 'Görlitz', '03': 'Cottbus', '04': 'Leipzig',
        '05': 'Chemnitz', '06': 'Halle', '07': 'Jena', '08': 'Zwickau', '09': 'Erfurt',
        '10': 'Berlin', '11': 'Berlin', '12': 'Berlin', '13': 'Berlin', '14': 'Berlin',
        '15': 'Berlin', '16': 'Berlin', '17': 'Berlin', '18': 'Berlin', '19': 'Berlin',
        '20': 'Hamburg', '21': 'Hamburg', '22': 'Hamburg', '23': 'Hamburg', '24': 'Hamburg', '25': 'Hamburg',
        '26': 'Bremen', '27': 'Bremen', '28': 'Bremen', '29': 'Bremen',
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
        '80': 'Munich', '81': 'Munich', '82': 'Munich', '83': 'Munich', '84': 'Munich', '85': 'Munich',
        '86': 'Augsburg', '87': 'Würzburg', '88': 'Ravensburg', '89': 'Ulm',
        '90': 'Nuremberg', '91': 'Nuremberg', '92': 'Nuremberg', '93': 'Regensburg',
        '94': 'Passau', '95': 'Bayreuth', '96': 'Bamberg', '97': 'Würzburg',
        '98': 'Coburg', '99': 'Erfurt'
      };

      const newCityName = prefixToCity[prefix];
      if (newCityName && currentName !== newCityName) {
        // Replace name
        const newEntry = fullMatch.replace(`name: "${currentName}"`, `name: "${newCityName}"`);
        germanySection = germanySection.replace(fullMatch, newEntry);
        replaceCount++;
      }
    }
  }
}

// Also replace area fields that contain company names
const areaPattern = /area: "([^"]*(?:GmbH|AG|KG|mbH|Deutsche Post|Universität|Agentur|Finanzamt|Landes|Stadtwerke|Sparkasse|Staatskanzlei|Aufbaubank|IHK|BKK|Rentenversicherung|Patentamt|Schwarzbierbrauerei|Bußgeldstelle|Stadtverwaltung|HUK-Coburg|AOK|Amtsgericht|Köstritzer|Mondelez|Familienkasse|Klinikum|Rundfunk|Bibliothek|Zeitung|Versicherung|Kasse|Werk|Bank|Brauerei)[^"]*)"/gi;

let areaMatch;
let areaReplaceCount = 0;
while ((areaMatch = areaPattern.exec(germanySection)) !== null) {
  const currentArea = areaMatch[1];
  // Find the postal code before this area
  const beforeArea = germanySection.substring(0, areaMatch.index);
  const codeMatch = beforeArea.match(/code: "(\d{5})"[^}]*$/);
  if (codeMatch) {
    const postalCode = codeMatch[1];
    const prefix = postalCode.substring(0, 2);
    const prefixToCity = {
      '01': 'Dresden', '02': 'Görlitz', '03': 'Cottbus', '04': 'Leipzig',
      '05': 'Chemnitz', '06': 'Halle', '07': 'Jena', '08': 'Zwickau', '09': 'Erfurt',
      '10': 'Berlin', '11': 'Berlin', '12': 'Berlin', '13': 'Berlin', '14': 'Berlin',
      '15': 'Berlin', '16': 'Berlin', '17': 'Berlin', '18': 'Berlin', '19': 'Berlin',
      '20': 'Hamburg', '21': 'Hamburg', '22': 'Hamburg', '23': 'Hamburg', '24': 'Hamburg', '25': 'Hamburg',
      '26': 'Bremen', '27': 'Bremen', '28': 'Bremen', '29': 'Bremen',
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
      '80': 'Munich', '81': 'Munich', '82': 'Munich', '83': 'Munich', '84': 'Munich', '85': 'Munich',
      '86': 'Augsburg', '87': 'Würzburg', '88': 'Ravensburg', '89': 'Ulm',
      '90': 'Nuremberg', '91': 'Nuremberg', '92': 'Nuremberg', '93': 'Regensburg',
      '94': 'Passau', '95': 'Bayreuth', '96': 'Bamberg', '97': 'Würzburg',
      '98': 'Coburg', '99': 'Erfurt'
    };
    const newArea = prefixToCity[prefix];
    if (newArea && currentArea !== newArea) {
      germanySection = germanySection.replace(`area: "${currentArea}"`, `area: "${newArea}"`);
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
