const fs = require('fs');

const content = fs.readFileSync('mockData.js', 'utf8');

// Extract all countries and their states/cities
const countryRegex = /\{ id: "([A-Z_]+)", name: "([^"]+)", states: \[/g;
const countries = [];
let match;

while ((match = countryRegex.exec(content)) !== null) {
  countries.push({ id: match[1], name: match[2], pos: match.index });
}

console.log('=== Data Integrity Check Report ===\n');
console.log(`Total countries found: ${countries.length}\n`);

let totalIssues = 0;
const problemCountries = [];

for (let i = 0; i < countries.length; i++) {
  const country = countries[i];
  const startPos = country.pos;
  const endPos = i < countries.length - 1 ? countries[i + 1].pos : content.length;
  const block = content.slice(startPos, endPos);

  // Count cities
  const cityMatches = block.match(/postalCodes:/g);
  const cityCount = cityMatches ? cityMatches.length : 0;

  // Count states
  const stateMatches = block.match(/cities: \[/g);
  const stateCount = stateMatches ? stateMatches.length : 0;

  if (cityCount < 10) {
    totalIssues++;
    problemCountries.push({
      id: country.id,
      name: country.name,
      cities: cityCount,
      states: stateCount
    });
  }
}

// Sort by city count ascending
problemCountries.sort((a, b) => a.cities - b.cities);

console.log('Countries with less than 10 cities:\n');
problemCountries.forEach(c => {
  console.log(`  ${c.name} (${c.id}): ${c.cities} cities, ${c.states} states`);
});

console.log(`\n=== Total: ${totalIssues} countries need data supplementation ===`);
