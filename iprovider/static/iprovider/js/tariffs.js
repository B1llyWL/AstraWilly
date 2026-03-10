class TariffsPage {
    constructor() {
        this.init();
    }

    init() {
        console.log('Tariffs page initialized');

        // Инициализируем выбор локации
        if (document.getElementById('country-select')) {
            new LocationSelector({
                countrySelectId: 'country-select',
                citySelectId: 'city-select',
                locationFormId: 'location-form'
            });
        }
        this.setupSpeedCalculator();
        this.initTooltips();
    }


    showTariffDetails(card) {
        const title = card.querySelector('.card-title').textContent;
        const details = card.querySelector('.card-text')?.textContent || 'No details available';

        // Можно открыть модальное окно с деталями
        console.log(`Showing details for: ${title}`, details);

        // Пример открытия модального окна Bootstrap
        const modal = new bootstrap.Modal(document.getElementById('tariffModal') || this.createModal());
        document.getElementById('tariffModalTitle').textContent = title;
        document.getElementById('tariffModalBody').textContent = details;
        modal.show();
    }


    createModal() {
        // Создаем модальное окно, если его нет
        const modalHTML = `
            <div class="modal fade" id="tariffModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="tariffModalTitle"></h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body" id="tariffModalBody"></div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Enable Tariff</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        return document.getElementById('tariffModal');
    }

    setupSpeedCalculator() {
        // Калькулятор скорости для тарифов
        const calculator = document.createElement('div');
        calculator.className = 'card mt-4';
        calculator.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${gettext('Speed Calculator')}</h5>
                <div class="mb-3">
                    <label for="tariffSpeed" class="form-label">${gettext('Select Tariff Speed (Mbps):')}</label>
                    <select class="form-select" id="tariffSpeed">
                        <option value="100">100 Mbps</option>
                        <option value="200">200 Mbps</option>
                        <option value="300">300 Mbps</option>
                        <option value="400">400 Mbps</option>
                        <option value="500">500 Mbps</option>
                        <option value="600">600 Mbps</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="downloadSize" class="form-label">${gettext('File Size to Download (GB):')}</label>
                    <input type="number" class="form-control" id="downloadSize" value="1" min="0.1" step="0.1">
                </div>
                <button class="btn btn-primary" id="calculateTime">${gettext('Calculate Download Time')}</button>
                <div id="result" class="mt-3" style="display: none;">
                    <div class="alert alert-info">
                        ${gettext('Download time:')} <span id="timeResult">0</span> ${gettext('minutes')}
                    </div>
                </div>
            </div>
        `;

        const moonWillySection = document.querySelector('.tariff-section');
        if (moonWillySection) {
            moonWillySection.appendChild(calculator);

            document.getElementById('calculateTime').addEventListener('click', () => {
                this.calculateDownloadTime();
            });
        }
    }

    calculateDownloadTime() {
        const speedMbps = parseFloat(document.getElementById('tariffSpeed').value);
        const sizeGB = parseFloat(document.getElementById('downloadSize').value);

        if (isNaN(speedMbps) || isNaN(sizeGB) || sizeGB <= 0) {
            this.showNotification('Please enter valid values', 'danger');
            return;
        }

        // Конвертация: GB → MB → Mb
        const sizeMb = sizeGB * 1024 * 8; // 1GB = 1024MB, 1MB = 8Mb
        const timeSeconds = sizeMb / speedMbps;
        const timeMinutes = timeSeconds / 60;

        document.getElementById('timeResult').textContent = timeMinutes.toFixed(2);
        document.getElementById('result').style.display = 'block';
    }

    initTooltips() {
        // Инициализация Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Добавляем tooltips к ценам
        const prices = document.querySelectorAll('.card-price');
        prices.forEach(price => {
            price.setAttribute('title', 'Click for more details');
            price.setAttribute('data-bs-toggle', 'tooltip');
            new bootstrap.Tooltip(price);
        });
    }

    showNotification(message, type = 'info') {
        // Та же функция, что и в ServicesPage
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '9999';
        notification.style.minWidth = '300px';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new TariffsPage();
});