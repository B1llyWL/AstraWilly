class LocationManager {
    constructor() {
        this.selectedCountryId = null;
        this.selectedCityId = null;
        this.init();
    }

    init() {
        console.log('Location manager initialized');
        this.setupNavLocation();
        this.setupPageLocation();
        this.setupClearButton();
        this.initGeolocation();
    }

    setupNavLocation() {
        const navCountry = document.getElementById('navCountry');
        const navCity = document.getElementById('navCity');

        if (navCountry) {
            navCountry.addEventListener('change', (e) => {
                this.loadCities(e.target.value, 'navCity');
            });
        }
    }

    setupPageLocation() {
        const pageCountry = document.getElementById('country-select');
        const pageCity = document.getElementById('city-select');

        if (pageCountry) {
            pageCountry.addEventListener('change', (e) => {
                this.loadCities(e.target.value, 'city-select');
            });
        }
    }

    setupClearButton() {
        const clearBtn = document.getElementById('clearLocationBtn');
        if(clearBtn) {
           clearBtn.addEventListener('click', (e) => {
               e.preventDefault();
               this.clearLocation();
           });
        }
    }

    async loadCities(countryId, citySelectId) {
        const citySelect = document.getElementById(citySelectId);
        if (!citySelect) return;

        if (!countryId) {
            citySelect.innerHTML = '<option value="">Select City (Optional)</option>';
            citySelect.disabled = true;
            return;
        }

        // Показываем загрузку
        citySelect.innerHTML = '<option value="">Loading cities...</option>';
        citySelect.disabled = true;

        try {
            const response = await fetch(`/get-cities/?country_id=${countryId}`);
            const data = await response.json();

            citySelect.innerHTML = '<option value="">Select City (Optional)</option>';

            if (data.cities && data.cities.length > 0) {
                data.cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = `${city.name}, ${city.country_name}`;
                    citySelect.appendChild(option);
                });
            citySelect.disabled = false;
        } else {
            citySelect.innerHTML = '<option value="">No cities available</option>';
            citySelect.disabled = true;
          }

        } catch (error) {
            console.error('Error loading cities:', error);
            citySelect.innerHTML = '<option value="">Error loading cities</option>';
            citySelect.disabled = false;
        }
    }

    initGeolocation() {
        const detectBtn = document.getElementById('detectLocationBtn');
        if (detectBtn){
            detectBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.detectUserLocation();
            });

        }
    }

    detectUserLocation() {
        if (!navigator.geolocation) {
            this.showNotification('Geolocation is not supported by your browser', 'warning');
            return;
        }

        this.showNotification('Detecting your location...', 'info');

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;
                await this.reverseGeocode(latitude, longitude);
            },
            (error) => {
                console.error('Geolocation error:', error);
                this.showNotification('Could not detect your location. Please select manually.', 'warning');
            }
        );
    }

    async reverseGeocode(latitude, longitude) {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`
            );
            const data = await response.json();

            if (data && data.address) {
                this.processGeocodeResult(data.address);
            }
        } catch (error) {
            console.error('Reverse geocoding error:', error);
            this.showNotification('Location detection failed. Please select manually.', 'warning');
        }
    }

    async processGeocodeResult(address) {
        const countryName = address.country;
        const cityName = address.city || address.town || address.village || null;

        if(!countryName) {
           this.showNotification('Could not determine your country.', 'warning');
           return;
        }

        try{
        const url = `/api/find-location/?country=${encodeURIComponent(countryName)}&city=${encodeURIComponent(cityName || '')}`;
        const response = await fetch(url);
        const data = await response.json();

        if(data.country_id) {
           const countrySelect = document.getElementById('navCountry');
           if(countrySelect) {
              countrySelect.value = data.country_id;
              countrySelect.dispatchEvent(new Event('change', {bubbles: true}));
              if (data.city_id) {
              const waitForCities = setInterval(() => {
                 const citySelect = document.getElementById('navCity');
                 if(citySelect && !citySelect.disabled) {
                 clearInterval(waitForCities);
                 citySelect.value = data.city_id;
                 this.showNotification(`Location set to ${cityName}, ${countryName}`,'success');
                 }
                }, 100);
                //Таймаут, если города не загрузятся
                setTimeout(() => clearInterval(waitForCities), 5000);
                } else{
                this.showNotification(`Location set to ${countryName}`,'success');
              }
           }
           } else {
               this.showNotification('Location not found in our database. Please select manually.', 'warning');
               }
           } catch(error) {
                console.error('Error finding location:', error);
                this.showNotification('Error processing location.', 'warning');
           }
        }
        clearLocation() {
            const form = document.getElementById('navLocationForm');
            if(form) {
                //Сбрасываем значения полей
                form.reset();
                //Отправляем форму, чтобы очистить сессию
                form.submit();
            }
        }

        //Внутренняя реализация уведомлений, если глобальна недоступна
        showNotification(message, type = 'info') {
            if(typeof window.showNotification === 'function') {
               window.showNotification(message,type);
            } else {
                console.log(`[${type.toUpperCase()}] ${message}`);
                alert(message); //fallback
            }
        }
    }

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    window.locationManager = new LocationManager();
});