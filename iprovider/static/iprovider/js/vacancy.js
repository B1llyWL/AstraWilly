class VacanciesPage {
    constructor() {
        this.init();
    }

    init() {
        console.log('Vacancies page initialized');

        // Инициализируем выбор локации
        if (document.getElementById('country-select')) {
            new LocationSelector({
                countrySelectId: 'country-select',
                citySelectId: 'city-select',
                locationFormId: 'location-form'
            });
        }

        // Инициализируем карточки вакансий
        this.initVacancyCards();
        this.initTooltips();
    }

    initVacancyCards() {
        const cards = document.querySelectorAll('.vacancy-card');

        cards.forEach(card => {
            // Добавляем обработчик клика для просмотра деталей
            const viewBtn = card.querySelector('.btn-primary');
            if (viewBtn) {
                viewBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.viewVacancyDetails(card);
                });
            }

            // Анимация при наведении на карточку
            card.addEventListener('mouseenter', () => {
                card.style.zIndex = '10';
            });

            card.addEventListener('mouseleave', () => {
                card.style.zIndex = '1';
            });

            // Обработчик для "more locations"
            const moreLocations = card.querySelector('.more-locations');
            if (moreLocations) {
                moreLocations.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const title = moreLocations.getAttribute('title');
                    this.showNotification(`Available locations: ${title}`, 'info');
                });
            }
        });
    }

    viewVacancyDetails(card) {
        const title = card.querySelector('.card-title').textContent;
        const description = card.querySelector('.vacancy-description p').textContent;
        const price = card.querySelector('.card-price h4').textContent;
        const category = card.querySelector('.vacancy-category-badge').textContent;
        const views = card.querySelector('.vacancy-views small').textContent;

        // Открываем модальное окно с деталями
        this.openVacancyModal({
            title,
            description,
            price,
            category,
            views,
            isPublished: card.querySelector('.badge-success') !== null
        });
    }

    openVacancyModal(data) {
        // Создаем модальное окно
        const modalId = 'vacancyDetailModal';
        let modal = document.getElementById(modalId);

        if (!modal) {
            modal = this.createModal(modalId);
        }

        // Заполняем данными
        document.getElementById('vacancyModalTitle').textContent = data.title;
        document.getElementById('vacancyModalCategory').textContent = data.category;
        document.getElementById('vacancyModalPrice').textContent = data.price;
        document.getElementById('vacancyModalViews').textContent = data.views;
        document.getElementById('vacancyModalDescription').textContent = data.description;

        // Показываем статус
        const statusBadge = document.getElementById('vacancyModalStatus');
        statusBadge.textContent = data.isPublished ? 'Published' : 'Draft';
        statusBadge.className = data.isPublished ? 'badge bg-success' : 'badge bg-secondary';

        // Открываем модальное окно
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }

    createModal(modalId) {
        const modalHTML = `
            <div class="modal fade" id="${modalId}" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="vacancyModalTitle"></h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-6">
                                    <span class="badge" id="vacancyModalCategory"></span>
                                    <span class="badge ms-2" id="vacancyModalStatus"></span>
                                </div>
                                <div class="col-md-6 text-end">
                                    <span id="vacancyModalViews" class="text-muted"></span>
                                </div>
                            </div>
                            <div class="mb-3">
                                <h4 id="vacancyModalPrice" class="text-primary"></h4>
                            </div>
                            <div class="mb-3">
                                <h6>Description:</h6>
                                <p id="vacancyModalDescription"></p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary" onclick="this.applyForVacancy()">Apply Now</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        return document.getElementById(modalId);
    }

    initTooltips() {
        // Инициализация Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    applyForVacancy() {
        this.showNotification('Application form will open shortly...', 'success');
    }

    showNotification(message, type = 'info') {
        const alertTypes = {
            'info': 'alert-info',
            'success': 'alert-success',
            'warning': 'alert-warning',
            'error': 'alert-danger'
        };

        const notification = document.createElement('div');
        notification.className = `alert ${alertTypes[type] || 'alert-info'} alert-dismissible fade show`;
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
    new VacanciesPage();
});