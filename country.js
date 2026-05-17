class CountryPage {
  constructor() {
    this.countryId = this.getCountryIdFromUrl();
    this.country = null;
    this.selectedCity = null;
    this.map = null;
    this.marker = null;
    this.nearbyMarkers = [];
    this.currentLayer = 'street';
    this.tileLayers = {};

    this.elements = {
      aboutCountryName: document.getElementById('about-country-name'),
      aboutCountry: document.getElementById('about-country'),
      aboutCountry2: document.getElementById('about-country-2'),
      aboutCountry3: document.getElementById('about-country-3'),
      citiesCountry: document.getElementById('cities-country'),
      citiesCountryNote: document.getElementById('cities-country-note'),
      pageTitle: document.getElementById('page-title'),
      pageDescription: document.getElementById('page-description'),
      citySearch: document.getElementById('city-search'),
      suggestionsList: document.getElementById('suggestions-list'),
      showBtn: document.getElementById('show-btn'),
      showSelectedBtn: document.getElementById('show-selected-btn'),
      citiesSelect: document.getElementById('cities-select'),
      statesContainer: document.getElementById('states-container'),
      resultsSection: document.getElementById('results-section'),
      postalDetails: document.getElementById('postal-details'),
      map: document.getElementById('map'),
      searchCountryFlag: document.getElementById('search-country-flag'),
      searchCountryName: document.getElementById('search-country-name')
    };

    this.countryNames = {
      'US': 'US', 'CA': 'Canada', 'JP': 'Japan', 'FR': 'France', 'ZA': 'South Africa',
      'UK': 'UK', 'BR': 'Brazil', 'DE': 'Germany', 'ID': 'Indonesia', 'PL': 'Poland',
      'IT': 'Italy', 'MX': 'Mexico', 'NO': 'Norway', 'IN': 'India', 'NZ': 'New Zealand',
      'AU': 'Australia', 'RU': 'Russia', 'CN': 'China', 'TR': 'Turkey', 'ES': 'Spain',
      'SE': 'Sweden', 'LT': 'Lithuania', 'GR': 'Greece', 'PR': 'Puerto Rico', 'TH': 'Thailand',
      'FI': 'Finland', 'PT': 'Portugal', 'BE': 'Belgium', 'DK': 'Denmark', 'HR': 'Croatia',
      'NL': 'Netherlands', 'HU': 'Hungary', 'AT': 'Austria', 'CH': 'Switzerland', 'CZ': 'Czech Republic',
      'SK': 'Slovakia', 'SG': 'Singapore', 'LU': 'Luxembourg'
    };

    this.init();
  }

  getCountryIdFromUrl() {
    // First check URL query params (for country.html?country=US)
    const params = new URLSearchParams(window.location.search);
    const countryFromQuery = params.get('country');
    if (countryFromQuery) return countryFromQuery;

    // Then check static page URL (for us-postal-code.html)
    const path = window.location.pathname;
    const match = path.match(/([a-z-]+)-postal-code\.html$/);
    if (match) {
      const slug = match[1];
      // Map slug back to country ID
      const slugToId = {
        'us': 'US',
        'canada': 'CA',
        'united-kingdom': 'UK',
        'germany': 'DE',
        'france': 'FR',
        'japan': 'JP',
        'india': 'IN',
        'australia': 'AU',
        'brazil': 'BR',
        'italy': 'IT',
        'spain': 'ES',
        'netherlands': 'NL',
        'sweden': 'SE',
        'norway': 'NO',
        'finland': 'FI',
        'denmark': 'DK',
        'poland': 'PL',
        'austria': 'AT',
        'switzerland': 'CH',
        'belgium': 'BE',
        'portugal': 'PT',
        'ireland': 'IE',
        'new-zealand': 'NZ',
        'south-africa': 'ZA',
        'mexico': 'MX',
        'russia': 'RU',
        'turkey': 'TR',
        'czech-republic': 'CZ',
        'hungary': 'HU',
        'slovakia': 'SK',
        'croatia': 'HR',
        'slovenia': 'SI',
        'lithuania': 'LT',
        'latvia': 'LV',
        'estonia': 'EE',
        'luxembourg': 'LU',
        'iceland': 'IS',
        'malta': 'MT',
        'china': 'CN',
        'indonesia': 'ID',
        'greece': 'GR',
        'singapore': 'SG',
        'thailand': 'TH',
        'malaysia': 'MY',
        'philippines': 'PH',
        'south-korea': 'KR',
        'uae': 'AE',
        'israel': 'IL'
      };
      return slugToId[slug] || null;
    }

    return null;
  }

  init() {
    if (!this.countryId || !postalData) {
      window.location.href = 'index.html';
      return;
    }

    this.country = postalData.countries.find(c => c.id === this.countryId);
    if (!this.country) {
      window.location.href = 'index.html';
      return;
    }

    this.updatePageInfo();
    this.renderCitiesSelect();
    this.renderStatesList();
    this.bindEvents();
  }

  updatePageInfo() {
    const displayName = this.countryNames[this.countryId] || this.country.name;
    
    // 国旗代码映射（某些国家代码与国旗文件名不同）
    const flagCodeMap = {
      'UK': 'gb'
    };
    const flagCode = flagCodeMap[this.countryId] || this.countryId.toLowerCase();

    document.title = `${displayName} Postal Code Lookup`;
    
    // 安全设置元素内容，检查元素是否存在
    if (this.elements.pageDescription) {
      this.elements.pageDescription.content = `Search postal codes for cities in ${displayName}. Find zip codes by city name or address.`;
    }

    if (this.elements.aboutCountryName) {
      this.elements.aboutCountryName.textContent = displayName;
    }
    if (this.elements.aboutCountry) {
      this.elements.aboutCountry.textContent = displayName;
    }
    if (this.elements.aboutCountry2) {
      this.elements.aboutCountry2.textContent = displayName;
    }
    if (this.elements.aboutCountry3) {
      this.elements.aboutCountry3.textContent = displayName;
    }
    if (this.elements.citiesCountry) {
      this.elements.citiesCountry.textContent = displayName;
    }
    if (this.elements.citiesCountryNote) {
      this.elements.citiesCountryNote.textContent = displayName;
    }

    // 更新搜索板块的国家标题和国旗
    if (this.elements.searchCountryName) {
      this.elements.searchCountryName.textContent = displayName;
    }
    if (this.elements.searchCountryFlag) {
      this.elements.searchCountryFlag.src = `flags/${flagCode}.png`;
      this.elements.searchCountryFlag.alt = `${displayName} flag`;
    }
  }

  getAllCities() {
    const cities = [];
    this.country.states.forEach(state => {
      state.cities.forEach(city => {
        cities.push({
          id: city.id,
          name: city.name,
          state: state.name,
          stateId: state.id,
          postalCodes: city.postalCodes,
          lat: city.lat,
          lng: city.lng
        });
      });
    });
    return cities.sort((a, b) => a.name.localeCompare(b.name));
  }

  renderCitiesSelect() {
    const cities = this.getAllCities();
    this.elements.citiesSelect.innerHTML = '<option value="">Select a city...</option>';

    cities.forEach(city => {
      const option = document.createElement('option');
      option.value = city.id;
      option.textContent = `${city.name} (${city.state})`;
      this.elements.citiesSelect.appendChild(option);
    });
  }

  renderStatesList() {
    const states = this.country.states.sort((a, b) => a.name.localeCompare(b.name));
    this.elements.statesContainer.innerHTML = '';

    states.forEach(state => {
      const link = document.createElement('a');
      link.href = `#state-${state.id}`;
      link.className = 'state-link';
      link.setAttribute('data-state-id', state.id);
      link.textContent = state.name;
      link.addEventListener('click', (e) => {
        e.preventDefault();
        this.filterCitiesByState(state.id);
      });
      this.elements.statesContainer.appendChild(link);
    });
  }

  filterCitiesByState(stateId) {
    const state = this.country.states.find(s => s.id === stateId);
    if (!state) return;

    // 高亮当前选中的州/省链接
    const stateLinks = this.elements.statesContainer.querySelectorAll('.state-link');
    stateLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('data-state-id') === stateId) {
        link.classList.add('active');
        // 滚动到选中的州/省（如果在可视区域外）
        link.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });

    // 显示所有城市，但高亮当前选中的州/省
    const allCities = this.getAllCities();
    this.elements.citiesSelect.innerHTML = '<option value="">Select a city...</option>';
    
    // 首先显示当前州/省的城市
    allCities.forEach(city => {
      if (city.stateId === stateId) {
        const option = document.createElement('option');
        option.value = city.id;
        option.textContent = `${city.name} (${city.state})`;
        this.elements.citiesSelect.appendChild(option);
      }
    });
    
    // 添加分隔线
    const separator = document.createElement('option');
    separator.disabled = true;
    separator.textContent = `--- ${state.name} ---`;
    this.elements.citiesSelect.insertBefore(separator, this.elements.citiesSelect.children[1]);
  }

  bindEvents() {
    // Search input with autocomplete
    this.elements.citySearch.addEventListener('input', (e) => this.handleSearch(e));
    this.elements.citySearch.addEventListener('keydown', (e) => this.handleKeydown(e));
    this.elements.citySearch.addEventListener('focus', () => this.showSuggestions());

    // Click outside to close suggestions
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.autocomplete-wrapper')) {
        this.hideSuggestions();
      }
    });

    // Show buttons
    this.elements.showBtn.addEventListener('click', () => this.showResults());
    this.elements.showSelectedBtn.addEventListener('click', () => this.showSelectedResults());

    // City select change
    this.elements.citiesSelect.addEventListener('change', (e) => {
      const cityId = e.target.value;
      if (cityId) {
        const cities = this.getAllCities();
        this.selectedCity = cities.find(c => c.id === cityId);
        this.elements.showBtn.disabled = false;
      } else {
        this.selectedCity = null;
        this.elements.showBtn.disabled = true;
      }
    });

    // Popular city links click handler
    document.querySelectorAll('.city-link-item').forEach(item => {
      item.style.cursor = 'pointer';
      item.addEventListener('click', () => {
        const cityName = item.getAttribute('data-city');
        if (cityName) {
          const cities = this.getAllCities();
          const city = cities.find(c => c.name === cityName);
          if (city) {
            this.selectCity(city);
            this.showResults();
            // Scroll to results section
            this.elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      });
    });
  }

  handleSearch(e) {
    const query = e.target.value.trim().toLowerCase();
    if (query.length === 0) {
      this.hideSuggestions();
      this.selectedCity = null;
      this.elements.showBtn.disabled = true;
      return;
    }

    const cities = this.getAllCities();
    const matches = cities.filter(city =>
      city.name.toLowerCase().includes(query) ||
      city.state.toLowerCase().includes(query)
    ).slice(0, 10);

    this.renderSuggestions(matches);
  }

  renderSuggestions(matches) {
    this.elements.suggestionsList.innerHTML = '';

    if (matches.length === 0) {
      this.hideSuggestions();
      return;
    }

    matches.forEach((city, index) => {
      const li = document.createElement('li');
      li.className = 'suggestion-item';
      li.setAttribute('role', 'option');
      li.setAttribute('data-index', index);
      li.innerHTML = `
        <span class="suggestion-city">${city.name}</span>
        <span class="suggestion-state"> (${city.state})</span>
      `;

      li.addEventListener('click', () => {
        this.selectCity(city);
      });

      this.elements.suggestionsList.appendChild(li);
    });

    this.showSuggestions();
  }

  handleKeydown(e) {
    const items = this.elements.suggestionsList.querySelectorAll('.suggestion-item');
    const highlighted = this.elements.suggestionsList.querySelector('.highlighted');
    let currentIndex = highlighted ? parseInt(highlighted.dataset.index) : -1;

    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        currentIndex = Math.min(currentIndex + 1, items.length - 1);
        this.highlightItem(items, currentIndex);
        break;
      case 'ArrowUp':
        e.preventDefault();
        currentIndex = Math.max(currentIndex - 1, 0);
        this.highlightItem(items, currentIndex);
        break;
      case 'Enter':
        e.preventDefault();
        if (highlighted) {
          highlighted.click();
        }
        break;
      case 'Escape':
        this.hideSuggestions();
        break;
    }
  }

  highlightItem(items, index) {
    items.forEach(item => item.classList.remove('highlighted'));
    if (items[index]) {
      items[index].classList.add('highlighted');
      items[index].scrollIntoView({ block: 'nearest' });
    }
  }

  selectCity(city) {
    this.selectedCity = city;
    this.elements.citySearch.value = city.name;
    this.elements.showBtn.disabled = false;
    this.hideSuggestions();

    // Also select the option in the dropdown
    this.elements.citiesSelect.value = city.id;
  }

  showSuggestions() {
    if (this.elements.suggestionsList.children.length > 0) {
      this.elements.suggestionsList.classList.add('active');
    }
  }

  hideSuggestions() {
    this.elements.suggestionsList.classList.remove('active');
  }

  showSelectedResults() {
    const cityId = this.elements.citiesSelect.value;
    if (!cityId) {
      this.showToast('Please select a city first');
      return;
    }

    const cities = this.getAllCities();
    this.selectedCity = cities.find(c => c.id === cityId);
    this.showResults();
  }

  async showResults() {
    if (!this.selectedCity) return;

    const city = this.selectedCity;
    const postalCodes = city.postalCodes;
    const primaryPostal = postalCodes[0];

    // Show results section
    this.elements.resultsSection.style.display = 'block';

    // Render postal code info with enhanced layout
    let postalCodesHtml = postalCodes.map((pc, index) => `
      <div class="postal-code-item ${index === 0 ? 'primary' : ''}">
        <div class="postal-code-number">${pc.code}</div>
        <div class="postal-code-area">${pc.area}</div>
        <button class="copy-btn-small" onclick="countryPage.copyToClipboard('${pc.code}')" title="Copy">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width: 16px; height: 16px;">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 01-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 011.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 00-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 01-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 00-3.375-3.375h-1.5" />
          </svg>
        </button>
      </div>
    `).join('');

    // Find nearby cities by real distance
    const nearbyCities = this.getNearbyCities(city);
    let nearbyHtml = '';
    if (nearbyCities.length > 0) {
      nearbyHtml = `
        <div class="nearby-section">
          <h4>Nearby Locations</h4>
          <div class="nearby-list">
            ${nearbyCities.map(nc => `
              <div class="nearby-item" onclick="countryPage.selectCityById('${nc.id}')">
                <span class="nearby-name">${nc.name}</span>
                <span class="nearby-distance">${nc.distance ? countryPage.formatDistance(nc.distance) : ''}</span>
                <span class="nearby-postal">${nc.postalCodes[0]?.code || ''}</span>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    this.elements.postalDetails.innerHTML = `
      <div class="location-header">
        <h3 class="location-name">${city.name}</h3>
        <p class="location-address">${city.state}, ${this.countryNames[this.countryId] || this.country.name}</p>
      </div>
      
      <div class="postal-codes-section">
        <h4>Postal Codes</h4>
        <div class="postal-codes-list">
          ${postalCodesHtml}
        </div>
      </div>
      
      ${nearbyHtml}
      
      <div class="location-details">
        <h4>Location Details</h4>
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">City:</span>
            <span class="detail-value">${city.name}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">State/Province:</span>
            <span class="detail-value">${city.state}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Country:</span>
            <span class="detail-value">${this.countryNames[this.countryId] || this.country.name}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Primary Postal Code:</span>
            <span class="detail-value">${primaryPostal.code}</span>
          </div>
        </div>
      </div>
    `;

    // Initialize or update map (async)
    await this.initMap(city);

    // Scroll to results
    setTimeout(() => {
      this.elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  getNearbyCities(city) {
    // 获取所有其他城市，按真实地理距离排序
    const allCities = [];
    this.country.states.forEach(s => {
      s.cities.forEach(c => {
        if (c.id !== city.id) {
          allCities.push({
            id: c.id,
            name: c.name,
            postalCodes: c.postalCodes,
            state: s.name,
            stateId: s.id,
            lat: c.lat,
            lng: c.lng
          });
        }
      });
    });

    // 如果有坐标，使用Haversine公式计算真实地理距离
    if (city.lat && city.lng) {
      allCities.forEach(c => {
        if (c.lat && c.lng) {
          c.distance = this.haversineDistance(city.lat, city.lng, c.lat, c.lng);
        } else {
          c.distance = Infinity;
        }
      });

      // 按距离排序
      allCities.sort((a, b) => a.distance - b.distance);
    } else {
      // 没有坐标时，优先显示同州/省的城市
      allCities.sort((a, b) => {
        const aSameState = a.stateId === city.stateId ? 0 : 1;
        const bSameState = b.stateId === city.stateId ? 0 : 1;
        return aSameState - bSameState;
      });
    }

    // 返回最近的5个城市
    return allCities.slice(0, 5);
  }

  haversineDistance(lat1, lng1, lat2, lng2) {
    // Haversine公式计算球面距离（单位：公里）
    const R = 6371; // 地球半径（公里）
    const dLat = this.toRadians(lat2 - lat1);
    const dLng = this.toRadians(lng2 - lng1);
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
              Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  toRadians(degrees) {
    return degrees * (Math.PI / 180);
  }

  formatDistance(distance) {
    // 格式化距离显示
    if (distance === Infinity || distance === undefined) return '';
    if (distance < 1) {
      return `${Math.round(distance * 1000)} m`;
    } else if (distance < 100) {
      return `${Math.round(distance * 10) / 10} km`;
    } else {
      return `${Math.round(distance)} km`;
    }
  }

  selectCityById(cityId) {
    const cities = this.getAllCities();
    const city = cities.find(c => c.id === cityId);
    if (city) {
      this.selectCity(city);
      this.showResults();
    }
  }

  async fetchCityCoordinates(city) {
    // 使用Nominatim API实时获取城市坐标
    const countryNames = {
      'US': 'United States', 'CA': 'Canada', 'JP': 'Japan', 'FR': 'France', 'ZA': 'South Africa',
      'UK': 'United Kingdom', 'BR': 'Brazil', 'DE': 'Germany', 'ID': 'Indonesia', 'PL': 'Poland',
      'IT': 'Italy', 'MX': 'Mexico', 'NO': 'Norway', 'IN': 'India', 'NZ': 'New Zealand',
      'AU': 'Australia', 'RU': 'Russia', 'CN': 'China', 'TR': 'Turkey', 'ES': 'Spain',
      'SE': 'Sweden', 'LT': 'Lithuania', 'GR': 'Greece', 'PR': 'Puerto Rico', 'TH': 'Thailand',
      'FI': 'Finland', 'PT': 'Portugal', 'BE': 'Belgium', 'DK': 'Denmark', 'HR': 'Croatia',
      'NL': 'Netherlands', 'HU': 'Hungary', 'AT': 'Austria', 'CH': 'Switzerland', 'CZ': 'Czech Republic',
      'SK': 'Slovakia', 'SG': 'Singapore', 'LU': 'Luxembourg', 'IE': 'Ireland', 'IL': 'Israel',
      'KR': 'South Korea', 'MY': 'Malaysia', 'PH': 'Philippines', 'AR': 'Argentina',
      'CL': 'Chile', 'CO': 'Colombia', 'PE': 'Peru', 'EG': 'Egypt',
      'NG': 'Nigeria', 'KE': 'Kenya', 'AE': 'United Arab Emirates', 'SA': 'Saudi Arabia'
    };

    const country = countryNames[this.countryId] || this.country.name;
    const query = encodeURIComponent(`${city.name}, ${country}`);
    const url = `https://nominatim.openstreetmap.org/search?q=${query}&format=json&limit=1`;

    try {
      const response = await fetch(url, {
        headers: { 'User-Agent': 'PostalCodeLookup/1.0' }
      });
      const data = await response.json();
      if (data && data.length > 0) {
        return {
          lat: parseFloat(data[0].lat),
          lng: parseFloat(data[0].lon)
        };
      }
    } catch (e) {
      console.warn('Failed to fetch coordinates:', e);
    }
    return null;
  }

  async initMap(city) {
    // 国家默认坐标
    const defaultCoords = {
      'US': [39.8283, -98.5795], 'CA': [56.1304, -106.3468], 'JP': [36.2048, 138.2529],
      'FR': [46.2276, 2.2137], 'ZA': [-30.5595, 22.9375], 'UK': [55.3781, -3.4360],
      'BR': [-14.2350, -51.9253], 'DE': [51.1657, 10.4515], 'ID': [-0.7893, 113.9213],
      'PL': [51.9194, 19.1451], 'IT': [41.8719, 12.5674], 'MX': [23.6345, -102.5528],
      'NO': [60.4720, 8.4689], 'IN': [20.5937, 78.9629], 'NZ': [-40.9006, 174.8860],
      'AU': [-25.2744, 133.7751], 'RU': [61.5240, 105.3188], 'CN': [35.8617, 104.1954],
      'TR': [38.9637, 35.2433], 'ES': [40.4637, -3.7492], 'SE': [60.1282, 18.6435],
      'LT': [55.1694, 23.8813], 'GR': [39.0742, 21.8243], 'PR': [18.2208, -66.5901],
      'TH': [15.8700, 100.9925], 'FI': [61.9241, 25.7482], 'PT': [39.3999, -8.2245],
      'BE': [50.5039, 4.4699], 'DK': [56.2639, 9.5018], 'HR': [45.1000, 15.2000],
      'NL': [52.1326, 5.2913], 'HU': [47.1625, 19.5033], 'AT': [47.5162, 14.5501],
      'CH': [46.8182, 8.2275], 'CZ': [49.8175, 15.4730], 'SK': [48.6690, 19.6990],
      'SG': [1.3521, 103.8198], 'LU': [49.8153, 6.1296]
    };

    // 优先使用已有坐标，否则实时获取
    let coords;
    let hasPreciseCoords = false;

    if (city.lat && city.lng) {
      coords = [city.lat, city.lng];
      hasPreciseCoords = true;
    } else {
      // 尝试实时获取坐标
      const fetchedCoords = await this.fetchCityCoordinates(city);
      if (fetchedCoords) {
        coords = [fetchedCoords.lat, fetchedCoords.lng];
        hasPreciseCoords = true;
        // 缓存坐标到城市数据
        city.lat = fetchedCoords.lat;
        city.lng = fetchedCoords.lng;
      } else {
        coords = defaultCoords[this.countryId] || [0, 0];
      }
    }

    const zoomLevel = hasPreciseCoords ? 12 : 6;

    if (!this.map) {
      this.map = L.map('map').setView(coords, zoomLevel);
      this.initTileLayers();
      this.addMapControls();
    } else {
      this.map.setView(coords, zoomLevel);
    }

    // 清除之前的标记
    this.clearMarkers();

    // 添加主标记（红色）
    const mainIcon = L.divIcon({
      className: 'custom-marker main-marker',
      html: '<div class="marker-pin"><span>📍</span></div>',
      iconSize: [40, 40],
      iconAnchor: [20, 40]
    });

    this.marker = L.marker(coords, { icon: mainIcon }).addTo(this.map)
      .bindPopup(`<b>${city.name}</b><br>Postal Code: ${city.postalCodes[0].code}<br><a href="${this.getStreetViewUrl(coords)}" target="_blank" class="street-view-link">🌎 View Street View</a>`)
      .openPopup();

    // 添加附近地点标记
    this.addNearbyMarkers(city, coords);
  }

  initTileLayers() {
    // 街道图
    this.tileLayers.street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    });

    // 卫星图（使用ESRI）
    this.tileLayers.satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
      maxZoom: 19
    });

    // 地形图
    this.tileLayers.terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
      maxZoom: 17
    });

    // 暗色主题
    this.tileLayers.dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19
    });

    // 默认显示街道图
    this.tileLayers.street.addTo(this.map);
  }

  addMapControls() {
    // 创建图层切换控件
    const layerControl = L.control({ position: 'topright' });
    layerControl.onAdd = () => {
      const div = L.DomUtil.create('div', 'layer-control');
      div.innerHTML = `
        <button class="layer-btn active" data-layer="street" title="Street Map">🗺️</button>
        <button class="layer-btn" data-layer="satellite" title="Satellite">🛰️</button>
        <button class="layer-btn" data-layer="terrain" title="Terrain">⛰️</button>
        <button class="layer-btn" data-layer="dark" title="Dark Mode">🌙</button>
      `;

      div.querySelectorAll('.layer-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.switchLayer(btn.dataset.layer);
          div.querySelectorAll('.layer-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        });
      });

      return div;
    };
    layerControl.addTo(this.map);

    // 添加街景链接控件
    const streetViewControl = L.control({ position: 'bottomright' });
    streetViewControl.onAdd = () => {
      const div = L.DomUtil.create('div', 'street-view-control');
      div.innerHTML = `<a href="#" class="street-view-btn" title="Open Street View">🌎 Street View</a>`;
      div.querySelector('.street-view-btn').addEventListener('click', (e) => {
        e.preventDefault();
        const center = this.map.getCenter();
        window.open(this.getStreetViewUrl([center.lat, center.lng]), '_blank');
      });
      return div;
    };
    streetViewControl.addTo(this.map);
  }

  switchLayer(layerName) {
    if (this.currentLayer === layerName) return;

    // 移除当前图层
    this.map.removeLayer(this.tileLayers[this.currentLayer]);

    // 添加新图层
    this.tileLayers[layerName].addTo(this.map);
    this.currentLayer = layerName;
  }

  getStreetViewUrl(coords) {
    const [lat, lng] = coords;
    return `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${lat},${lng}`;
  }

  clearMarkers() {
    if (this.marker) {
      this.map.removeLayer(this.marker);
      this.marker = null;
    }
    this.nearbyMarkers.forEach(marker => this.map.removeLayer(marker));
    this.nearbyMarkers = [];
  }

  addNearbyMarkers(city, mainCoords) {
    const nearbyCities = this.getNearbyCities(city);
    const nearbyIcon = L.divIcon({
      className: 'custom-marker nearby-marker',
      html: '<div class="marker-pin nearby"><span>📌</span></div>',
      iconSize: [30, 30],
      iconAnchor: [15, 30]
    });

    nearbyCities.forEach((nearby, index) => {
      if (nearby.lat && nearby.lng) {
        const marker = L.marker([nearby.lat, nearby.lng], { icon: nearbyIcon })
          .addTo(this.map)
          .bindPopup(`<b>${nearby.name}</b><br>Distance: ${this.formatDistance(nearby.distance)}<br>Postal: ${nearby.postalCodes[0]?.code || ''}<br><a href="${this.getStreetViewUrl([nearby.lat, nearby.lng])}" target="_blank">🌎 Street View</a>`);
        this.nearbyMarkers.push(marker);
      }
    });

    // 如果有附近标记，调整地图视野以显示所有标记
    if (this.nearbyMarkers.length > 0) {
      const group = new L.featureGroup([this.marker, ...this.nearbyMarkers]);
      this.map.fitBounds(group.getBounds().pad(0.1));
    }
  }

  async copyToClipboard(code) {
    try {
      await navigator.clipboard.writeText(code);
      this.showToast(`Copied: ${code}`);
    } catch (err) {
      const textArea = document.createElement('textarea');
      textArea.value = code;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
      this.showToast(`Copied: ${code}`);
    }
  }

  showToast(message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('hiding');
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 300);
    }, 2500);
  }
}

let countryPage;
document.addEventListener('DOMContentLoaded', () => {
  countryPage = new CountryPage();
});
