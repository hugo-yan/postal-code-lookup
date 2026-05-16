class ZipFinderApp {
  constructor() {
    this.countrySelect = document.getElementById('country-select');
    this.stateSelect = document.getElementById('state-select');
    this.citySelect = document.getElementById('city-select');
    this.searchInput = document.getElementById('search-input');
    this.resultsContainer = document.getElementById('results-container');
    this.adInline = document.getElementById('ad-inline');

    this.debounceTimer = null;
    this.currentResults = [];

    this.init();
  }

  init() {
    this.populateCountries();
    this.bindEvents();
    this.updateStats();
  }

  bindEvents() {
    this.countrySelect.addEventListener('change', (e) => this.onCountryChange(e));
    this.stateSelect.addEventListener('change', (e) => this.onStateChange(e));
    this.citySelect.addEventListener('change', (e) => this.onCityChange(e));
    this.searchInput.addEventListener('input', (e) => this.onSearchInput(e));
  }

  populateCountries() {
    const defaultOption = this.countrySelect.querySelector('option:first-child');
    this.countrySelect.innerHTML = '';
    this.countrySelect.appendChild(defaultOption);

    postalData.countries.forEach(country => {
      const option = document.createElement('option');
      option.value = country.id;
      option.textContent = country.name;
      this.countrySelect.appendChild(option);
    });
  }

  onCountryChange(e) {
    const countryId = e.target.value;

    if (!countryId) {
      this.resetStateSelect();
      this.resetCitySelect();
      this.clearResults();
      return;
    }

    const country = postalData.countries.find(c => c.id === countryId);
    if (!country) return;

    this.populateStates(country.states);
    this.resetCitySelect();
    this.clearResults();
  }

  populateStates(states) {
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'All states / provinces';

    this.stateSelect.innerHTML = '';
    this.stateSelect.appendChild(defaultOption);
    this.stateSelect.disabled = false;

    states.forEach(state => {
      const option = document.createElement('option');
      option.value = state.id;
      option.textContent = state.name;
      this.stateSelect.appendChild(option);
    });
  }

  onStateChange(e) {
    const stateId = e.target.value;
    const countryId = this.countrySelect.value;

    if (!stateId || !countryId) {
      this.resetCitySelect();
      this.clearResults();
      return;
    }

    const country = postalData.countries.find(c => c.id === countryId);
    if (!country) return;

    const state = country.states.find(s => s.id === stateId);
    if (!state) return;

    this.populateCities(state.cities);

    if (!this.searchInput.value.trim()) {
      this.displayResults(postalData.getPostalCodesByLocation(countryId, stateId));
    }
  }

  populateCities(cities) {
    const allCitiesOption = document.createElement('option');
    allCitiesOption.value = '';
    allCitiesOption.textContent = 'All cities';

    this.citySelect.innerHTML = '';
    this.citySelect.appendChild(allCitiesOption);

    cities.forEach(city => {
      const option = document.createElement('option');
      option.value = city.id;
      option.textContent = city.name;
      this.citySelect.appendChild(option);
    });
  }

  onCityChange(e) {
    const countryId = this.countrySelect.value;
    const stateId = this.stateSelect.value;
    const cityId = e.target.value;

    if (!this.searchInput.value.trim()) {
      if (cityId) {
        this.displayResults(postalData.getPostalCodesByLocation(countryId, stateId, cityId));
      } else if (stateId) {
        this.displayResults(postalData.getPostalCodesByLocation(countryId, stateId));
      }
    }
  }

  onSearchInput(e) {
    clearTimeout(this.debounceTimer);

    this.debounceTimer = setTimeout(() => {
      const query = e.target.value.trim();

      if (query.length === 0) {
        this.onDropdownSelection();
        return;
      }

      this.performSearch(query);
    }, 200);
  }

  onDropdownSelection() {
    const countryId = this.countrySelect.value;
    const stateId = this.stateSelect.value;
    const cityId = this.citySelect.value;

    if (cityId) {
      this.displayResults(postalData.getPostalCodesByLocation(countryId, stateId, cityId));
    } else if (stateId) {
      this.displayResults(postalData.getPostalCodesByLocation(countryId, stateId));
    } else if (countryId) {
      let results = [];
      const country = postalData.countries.find(c => c.id === countryId);
      if (country) {
        country.states.forEach(state => {
          results = results.concat(postalData.getPostalCodesByLocation(countryId, state.id));
        });
      }
      this.displayResults(results);
    } else {
      this.clearResults();
    }
  }

  performSearch(query) {
    const results = postalData.searchAll(query);
    this.displayResults(results);
  }

  displayResults(data) {
    this.currentResults = data;

    if (data.length === 0) {
      this.showNoResults();
      return;
    }

    const adThreshold = Math.ceil(data.length / 2);
    
    let html = `
      <div class="results-header">
        <span class="results-count">Found <strong>${data.length}</strong> postal code${data.length !== 1 ? 's' : ''}</span>
      </div>
      <table class="results-table" role="table" aria-label="Postal code search results">
        <thead>
          <tr>
            <th scope="col">Postal Code</th>
            <th scope="col">Area / Street</th>
            <th scope="col">City</th>
            <th scope="col">State / Province</th>
            <th scope="col">Country</th>
            <th scope="col">Type</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
    `;

    data.forEach((item, index) => {
      html += `
        <tr>
          <td class="postal-code-cell" aria-label="Postal code: ${item.code}">${this.escapeHtml(item.code)}</td>
          <td>${this.escapeHtml(item.area)}</td>
          <td>${this.escapeHtml(item.city)}</td>
          <td>${this.escapeHtml(item.state)}</td>
          <td>${this.escapeHtml(item.country)}</td>
          <td><span style="font-size: 0.8125rem; color: var(--color-text-muted);">${item.type}</span></td>
          <td>
            <button 
              class="copy-btn" 
              onclick="app.copyToClipboard('${this.escapeHtml(item.code)}', this)"
              aria-label="Copy postal code ${this.escapeHtml(item.code)} to clipboard"
              title="Copy to clipboard"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0 0 13.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
              </svg>
            </button>
          </td>
        </tr>
      `;

      if (index === adThreshold - 1 && data.length > 5) {
        html += `
          <tr>
            <td colspan="7" style="padding: 0;">
              <div class="ad-slot ad-slot-inline" style="margin: 0; border-radius: 0; border-left: none; border-right: none;">
                <span style="color: var(--color-text-muted); font-size: 0.8125rem;">In-Feed Advertisement</span>
              </div>
            </td>
          </tr>
        `;
      }
    });

    html += `
        </tbody>
      </table>
    `;

    this.resultsContainer.innerHTML = html;
    this.showAdInline(data.length > 5);
    this.scrollToResults();
  }

  showNoResults() {
    this.resultsContainer.innerHTML = `
      <div class="no-results">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
        </svg>
        <p><strong>No postal codes found.</strong></p>
        <p style="font-size: 0.9375rem; margin-top: var(--space-sm);">Try adjusting your search terms or location filters.</p>
      </div>
    `;
    this.hideAdInline();
  }

  clearResults() {
    this.resultsContainer.innerHTML = '';
    this.currentResults = [];
    this.hideAdInline();
  }

  async copyToClipboard(code, buttonElement) {
    try {
      await navigator.clipboard.writeText(code);
      this.showCopyFeedback(buttonElement);
      this.showToast(`Copied: ${code}`);
    } catch (err) {
      console.error('Failed to copy:', err);
      this.fallbackCopy(code, buttonElement);
    }
  }

  fallbackCopy(code, buttonElement) {
    const textArea = document.createElement('textarea');
    textArea.value = code;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
      document.execCommand('copy');
      this.showCopyFeedback(buttonElement);
      this.showToast(`Copied: ${code}`);
    } catch (err) {
      console.error('Fallback copy failed:', err);
      this.showToast('Copy failed. Please copy manually.', true);
    }
    
    document.body.removeChild(textArea);
  }

  showCopyFeedback(button) {
    button.classList.add('copied');
    button.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
    `;

    setTimeout(() => {
      button.classList.remove('copied');
      button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0 0 13.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
        </svg>
      `;
    }, 1500);
  }

  showToast(message, isError = false) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${isError ? 'error' : ''}`;
    toast.style.background = isError ? 'var(--color-error)' : 'var(--color-success)';
    
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

  scrollToResults() {
    setTimeout(() => {
      const resultsSection = document.getElementById('results');
      if (resultsSection && this.currentResults.length > 0) {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }

  showAdInline(show) {
    if (show && this.currentResults.length > 5) {
      this.adInline.style.display = 'block';
    } else {
      this.adInline.style.display = 'none';
    }
  }

  hideAdInline() {
    this.adInline.style.display = 'none';
  }

  resetStateSelect() {
    this.stateSelect.innerHTML = '<option value="">First select a country</option>';
    this.stateSelect.disabled = true;
  }

  resetCitySelect() {
    this.citySelect.innerHTML = '<option value="">All cities (optional)</option>';
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  updateStats() {
    const totalCodes = postalData.getTotalCount();
    let totalStates = 0;
    let totalCities = 0;

    postalData.countries.forEach(country => {
      totalStates += country.states.length;
      country.states.forEach(state => {
        totalCities += state.cities.length;
      });
    });

    const statCountries = document.getElementById('stat-countries');
    const statStates = document.getElementById('stat-states');
    const statCities = document.getElementById('stat-cities');
    const statTotal = document.getElementById('stat-total');

    if (statCountries) statCountries.textContent = postalData.countries.length;
    if (statStates) statStates.textContent = totalStates;
    if (statCities) statCities.textContent = totalCities;
    if (statTotal) statTotal.textContent = totalCodes;
  }
}

let app;
document.addEventListener('DOMContentLoaded', () => {
  app = new ZipFinderApp();
});
