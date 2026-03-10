/**
 * Управление выбором локации (страна/город)
 */

class LocationSelector {
    constructor(options = {}) {
        this.countrySelect = document.getElementById(options.countrySelectId || 'country-select');
        this.citySelect = document.getElementById(options.citySelectId || 'city-select');
        this.locationForm = document.getElementById(options.locationFormId || 'location-form');
        this.csrfToken = options.csrfToken || this.getCsrfToken();
        this.init();
    }

    init() {
        if (this.countrySelect && this.citySelect) {
            this.setupCountryChange();
        }

        if (this.locationForm) {
            this.setupFormSubmit();
        }
    }

    setupCountryChange() {
        this.countrySelect.addEventListener('change', () => {
            const countryId = this.countrySelect.value;

            if (countryId) {
                this.showCityLoading();
                this.loadCities(countryId);
            } else {
                this.disableCitySelect();
            }
        });
    }

    showCityLoading() {
        this.citySelect.innerHTML = '<option value="">Loading cities...</option>';
        this.citySelect.disabled = true;
    }

    disableCitySelect() {
        this.citySelect.innerHTML = '<option value="">First select the country</option>';
        this.citySelect.disabled = true;
    }

    async loadCities(countryId) {
        try {
            const response = await fetch(`/get-cities/?country_id=${countryId}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.updateCitySelect(data.cities);
        } catch (error) {
            console.error('Error loading cities:', error);
            this.showCityError();
        }
    }

    updateCitySelect(cities) {
        this.citySelect.innerHTML = '<option value="">Choose a city</option>';

        if (cities && cities.length > 0) {
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.id;
                option.textContent = city.name;
                this.citySelect.appendChild(option);
            });
            this.citySelect.disabled = false;
        } else {
            this.citySelect.innerHTML = '<option value="">There are no available cities</option>';
            this.citySelect.disabled = false;
        }
    }

    showCityError() {
        this.citySelect.innerHTML = '<option value="">Error loading cities</option>';
        this.citySelect.disabled = false;
    }

    setupFormSubmit() {
        this.locationForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            try {
                const formData = new FormData(this.locationForm);
                formData.append('csrfmiddlewaretoken', this.csrfToken);

                const response = await fetch(this.locationForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Error submitting form:', response.status);
                    this.showFormError();
                }
            } catch (error) {
                console.error('Error setting location:', error);
                this.showFormError();
            }
        });
    }

    getCsrfToken() {
        // Получаем CSRF токен из куки или мета-тега
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];

        if (cookieValue) {
            return cookieValue;
        }

        // Ищем в мета-тегах
        const metaToken = document.querySelector('meta[name="csrf-token"]');
        if (metaToken) {
            return metaToken.getAttribute('content');
        }

        return '';
    }

    showFormError() {
        // Можно добавить уведомление для пользователя
        alert('Error when setting the location. Please try again.');
    }
}

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LocationSelector;
} else {
    window.LocationSelector = LocationSelector;
}