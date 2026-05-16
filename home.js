class HomePage {
  constructor() {
    this.countriesGrid = document.getElementById('countries-grid');
    this.init();
  }

  init() {
    this.renderHotCountries();
  }

  getHotCountries() {
    // Based on Google search trends and postal code lookup popularity
    // Ordered by search volume / popularity (highest first)
    return [
      { id: 'US', code: 'US', flag: 'us', name: 'US', hot: true },
      { id: 'UK', code: 'GB', flag: 'gb', name: 'UK', hot: true },
      { id: 'CA', code: 'CA', flag: 'ca', name: 'Canada', hot: true },
      { id: 'AU', code: 'AU', flag: 'au', name: 'Australia', hot: true },
      { id: 'DE', code: 'DE', flag: 'de', name: 'Germany', hot: true },
      { id: 'FR', code: 'FR', flag: 'fr', name: 'France', hot: true },
      { id: 'IN', code: 'IN', flag: 'in', name: 'India', hot: true },
      { id: 'JP', code: 'JP', flag: 'jp', name: 'Japan', hot: true },
      { id: 'BR', code: 'BR', flag: 'br', name: 'Brazil', hot: true },
      { id: 'IT', code: 'IT', flag: 'it', name: 'Italy', hot: true },
      { id: 'ES', code: 'ES', flag: 'es', name: 'Spain', hot: false },
      { id: 'NL', code: 'NL', flag: 'nl', name: 'Netherlands', hot: false },
      { id: 'MX', code: 'MX', flag: 'mx', name: 'Mexico', hot: false },
      { id: 'RU', code: 'RU', flag: 'ru', name: 'Russia', hot: false },
      { id: 'CN', code: 'CN', flag: 'cn', name: 'China', hot: false },
      { id: 'ZA', code: 'ZA', flag: 'za', name: 'South Africa', hot: false },
      { id: 'SE', code: 'SE', flag: 'se', name: 'Sweden', hot: false },
      { id: 'NO', code: 'NO', flag: 'no', name: 'Norway', hot: false },
      { id: 'PL', code: 'PL', flag: 'pl', name: 'Poland', hot: false },
      { id: 'ID', code: 'ID', flag: 'id', name: 'Indonesia', hot: false },
      { id: 'TR', code: 'TR', flag: 'tr', name: 'Turkey', hot: false },
      { id: 'BE', code: 'BE', flag: 'be', name: 'Belgium', hot: false },
      { id: 'CH', code: 'CH', flag: 'ch', name: 'Switzerland', hot: false },
      { id: 'AT', code: 'AT', flag: 'at', name: 'Austria', hot: false },
      { id: 'DK', code: 'DK', flag: 'dk', name: 'Denmark', hot: false },
      { id: 'FI', code: 'FI', flag: 'fi', name: 'Finland', hot: false },
      { id: 'NZ', code: 'NZ', flag: 'nz', name: 'New Zealand', hot: false },
      { id: 'PT', code: 'PT', flag: 'pt', name: 'Portugal', hot: false },
      { id: 'GR', code: 'GR', flag: 'gr', name: 'Greece', hot: false },
      { id: 'CZ', code: 'CZ', flag: 'cz', name: 'Czech Republic', hot: false },
      { id: 'HU', code: 'HU', flag: 'hu', name: 'Hungary', hot: false },
      { id: 'IE', code: 'IE', flag: 'ie', name: 'Ireland', hot: false },
      { id: 'SG', code: 'SG', flag: 'sg', name: 'Singapore', hot: false },
      { id: 'TH', code: 'TH', flag: 'th', name: 'Thailand', hot: false },
      { id: 'MY', code: 'MY', flag: 'my', name: 'Malaysia', hot: false },
      { id: 'PH', code: 'PH', flag: 'ph', name: 'Philippines', hot: false },
      { id: 'KR', code: 'KR', flag: 'kr', name: 'South Korea', hot: false },
      { id: 'AE', code: 'AE', flag: 'ae', name: 'UAE', hot: false },
      { id: 'IL', code: 'IL', flag: 'il', name: 'Israel', hot: false }
    ];
  }

  renderHotCountries() {
    if (!this.countriesGrid) return;

    const countries = this.getHotCountries();

    countries.forEach(country => {
      const link = document.createElement('a');
      link.className = 'country-link';
      link.href = `country.html?country=${country.id}`;

      link.innerHTML = `
        <img class="country-flag-img" src="flags/${country.flag}.png" alt="${country.name} flag" width="20" height="15">
        <span class="country-code">${country.code}</span>
        <span class="country-name">${country.name} Postal Code Lookup</span>
        ${country.hot ? '<span class="hot-badge">HOT</span>' : ''}
      `;

      this.countriesGrid.appendChild(link);
    });
  }
}

let homePage;
document.addEventListener('DOMContentLoaded', () => {
  homePage = new HomePage();
});
