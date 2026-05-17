// 数据完整性检查脚本
const fs = require('fs');

// 读取 mockData.js
const dataContent = fs.readFileSync('mockData.js', 'utf8');

// 提取国家数据（简化解析）
const countries = [];
const countryMatches = dataContent.matchAll(/\{[\s\S]*?id:\s*"([A-Z]{2})"[\s\S]*?name:\s*"([^"]+)"[\s\S]*?states:\s*\[([\s\S]*?)\]\s*\}/g);

let match;
while ((match = countryMatches.next()) && !match.done) {
  const countryId = match.value[1];
  const countryName = match.value[2];
  const statesContent = match.value[3];
  
  // 统计州/省数量
  const stateCount = (statesContent.match(/\{[\s\S]*?id:\s*"/g) || []).length;
  
  // 统计城市数量
  const cityCount = (statesContent.match(/name:\s*"/g) || []).length;
  
  // 统计邮编数量
  const postalCodeCount = (statesContent.match(/code:\s*"/g) || []).length;
  
  // 检查是否有坐标数据
  const hasCoords = statesContent.includes('lat:') && statesContent.includes('lng:');
  const coordCount = (statesContent.match(/lat:/g) || []).length;
  
  countries.push({
    id: countryId,
    name: countryName,
    states: stateCount,
    cities: cityCount,
    postalCodes: postalCodeCount,
    hasCoords: hasCoords,
    coordCount: coordCount
  });
}

// 生成报告
console.log('='.repeat(80));
console.log('数据完整性检查报告');
console.log('='.repeat(80));
console.log(`\n总国家数: ${countries.length}\n`);

// 按城市数量排序
countries.sort((a, b) => b.cities - a.cities);

console.log('国家数据概览（按城市数量排序）：');
console.log('-'.repeat(80));
console.log(`${'国家'.padEnd(20)} ${'ID'.padEnd(6)} ${'州/省'.padEnd(8)} ${'城市'.padEnd(8)} ${'邮编'.padEnd(10)} ${'坐标'.padEnd(8)} ${'状态'}`);
console.log('-'.repeat(80));

countries.forEach(country => {
  const status = country.cities < 10 ? '⚠️ 数据不足' : 
                 country.cities < 50 ? '⚡ 需要补充' : '✅ 数据充足';
  const coordStatus = country.coordCount > 0 ? `${country.coordCount}个` : '❌ 缺失';
  
  console.log(
    `${country.name.padEnd(20)} ${country.id.padEnd(6)} ${String(country.states).padEnd(8)} ${String(country.cities).padEnd(8)} ${String(country.postalCodes).padEnd(10)} ${coordStatus.padEnd(8)} ${status}`
  );
});

// 问题统计
console.log('\n' + '='.repeat(80));
console.log('问题统计');
console.log('='.repeat(80));

const lowDataCountries = countries.filter(c => c.cities < 10);
const noCoordCountries = countries.filter(c => c.coordCount === 0);
const mediumDataCountries = countries.filter(c => c.cities >= 10 && c.cities < 50);

console.log(`\n🔴 数据严重不足（<10个城市）: ${lowDataCountries.length} 个国家`);
if (lowDataCountries.length > 0) {
  lowDataCountries.forEach(c => {
    console.log(`   - ${c.name} (${c.id}): ${c.cities} 个城市, ${c.postalCodes} 个邮编`);
  });
}

console.log(`\n🟡 数据需要补充（10-50个城市）: ${mediumDataCountries.length} 个国家`);
if (mediumDataCountries.length > 0) {
  mediumDataCountries.forEach(c => {
    console.log(`   - ${c.name} (${c.id}): ${c.cities} 个城市, ${c.postalCodes} 个邮编`);
  });
}

console.log(`\n❌ 缺少坐标数据: ${noCoordCountries.length} 个国家`);
if (noCoordCountries.length > 0) {
  noCoordCountries.forEach(c => {
    console.log(`   - ${c.name} (${c.id})`);
  });
}

// 生成详细建议
console.log('\n' + '='.repeat(80));
console.log('修复建议');
console.log('='.repeat(80));

if (lowDataCountries.length > 0) {
  console.log('\n1. 数据严重不足的国家需要优先补充数据：');
  lowDataCountries.forEach(c => {
    console.log(`   - ${c.name} (${c.id}): 建议至少补充到 50+ 个城市`);
  });
}

if (noCoordCountries.length > 0) {
  console.log('\n2. 缺少坐标数据的国家：');
  console.log('   建议为所有主要城市添加 lat/lng 坐标，以支持地图显示和附近城市功能');
  console.log('   可以通过 Nominatim API 批量获取坐标');
}

console.log('\n3. 数据增强建议：');
console.log('   - 为每个城市添加更多邮编（目前很多城市只有1个邮编）');
console.log('   - 为所有国家补充坐标数据');
console.log('   - 添加城市别名/多语言名称支持');
console.log('   - 添加邮编类型信息（Standard, PO Box, Military 等）');

// 保存报告
const reportContent = JSON.stringify({
  totalCountries: countries.length,
  lowDataCountries: lowDataCountries.map(c => ({ id: c.id, name: c.name, cities: c.cities })),
  mediumDataCountries: mediumDataCountries.map(c => ({ id: c.id, name: c.name, cities: c.cities })),
  noCoordCountries: noCoordCountries.map(c => ({ id: c.id, name: c.name })),
  allCountries: countries
}, null, 2);

fs.writeFileSync('data-check-report.json', reportContent);
console.log('\n✅ 详细报告已保存到 data-check-report.json');
