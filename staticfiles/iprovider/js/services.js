/**
 * Функциональность страницы услуг
 */

class ServicesPage {
    constructor() {
        this.init();
    }

    init() {
        console.log('Services page initialized');

        // Инициализируем выбор локации
        if (document.getElementById('country-select')) {
            new LocationSelector({
                countrySelectId: 'country-select',
                citySelectId: 'city-select',
                locationFormId: 'location-form'
            });
        }

        // Дополнительная логика для страницы услуг
        this.setupServiceCards();
        this.setupPriceHover();
    }

    setupServiceCards() {
        const cards = document.querySelectorAll('.card');

        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
                card.style.transition = 'transform 0.3s ease';
                card.style.boxShadow = '0 10px 20px rgba(0,0,0,0.1)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '';
            });

            // Клик по кнопке "Enable"
            const enableBtn = card.querySelector('.btn-outline-dark');
            if (enableBtn) {
                enableBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.handleEnableService(card);
                });
            }
        });
    }

    setupPriceHover() {
        const prices = document.querySelectorAll('.card-price h4');

        prices.forEach(price => {
            price.addEventListener('mouseenter', () => {
                price.style.color = '#0d6efd';
                price.style.transition = 'color 0.3s ease';
            });

            price.addEventListener('mouseleave', () => {
                price.style.color = '';
            });
        });
    }

    handleEnableService(card) {
        const serviceTitle = card.querySelector('.card-title').textContent;
        const price = card.querySelector('.text-primary').textContent;

        console.log(`Enabling service: ${serviceTitle} for ${price}`);

        // Здесь можно добавить логику добавления в корзину или AJAX запрос
        // Например:
        // this.addToCart(serviceTitle, price);

        // Временное уведомление
        this.showNotification(`Service "${serviceTitle}" added to cart!`, 'success');
    }

    showNotification(message, type = 'info') {
        // Создаем уведомление
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

        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    addToCart(serviceTitle, price) {
        // Пример AJAX запроса для добавления в корзину
        fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            },
            body: JSON.stringify({
                service: serviceTitle,
                price: parseFloat(price.replace('$', '')),
                quantity: 1
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Service added to cart successfully!', 'success');
            } else {
                this.showNotification('Error adding to cart', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showNotification('Network error', 'danger');
        });
    }

    getCsrfToken() {
        // Аналогично LocationSelector
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new ServicesPage();
});