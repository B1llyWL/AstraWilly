// Используем переменные, переданные из шаблона
const stripePublicKey = window.stripePublicKey;
const createCheckoutUrl = window.createCheckoutUrl;
const csrfToken = window.csrfToken;
const translations = window.translations || {};

// Инициализация Stripe
const stripe = Stripe(stripePublicKey);

// Элементы формы
const form = document.getElementById('payment-form');
const amountInput = document.getElementById('amount');
const currencySelect = document.getElementById('currency');
const payBtn = document.getElementById('pay-btn');
const messagesContainer = document.getElementById('payment-messages');

// Функция для отображения ошибок
function showMessage(message, type = 'danger') {
    messagesContainer.innerHTML = `<div class="alert alert-${type}" role="alert">${message}</div>`;
}

// Функция очистки сообщений
function clearMessages() {
    messagesContainer.innerHTML = '';
}

// Автоподстановка валюты при выборе страны
const countrySelect = document.getElementById('country');
if (countrySelect && currencySelect) {
    countrySelect.addEventListener('change', function() {
        const selectedOption = countrySelect.options[countrySelect.selectedIndex];
        const currency = selectedOption.getAttribute('data-currency');
        if (currency) {
            for (let i = 0; i < currencySelect.options.length; i++) {
                if (currencySelect.options[i].value === currency) {
                    currencySelect.selectedIndex = i;
                    break;
                }
            }
        }
    });
}

// Обработка отправки формы
form.addEventListener('submit', function(e) {
    e.preventDefault();
    clearMessages();

    const amount = amountInput.value;
    const currency = currencySelect.value;

    // Валидация
    if (!amount || parseFloat(amount) <= 0) {
        showMessage(translations.validAmount || 'Please enter a valid amount.', 'warning');
        return;
    }

    // Блокируем кнопку
    payBtn.disabled = true;
    payBtn.textContent = translations.processing || 'Processing...';

    // Отправка запроса на создание сессии
    fetch(createCheckoutUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams({
            'amount': amount,
            'currency': currency,
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || translations.serverError || 'Server error');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        // Редирект на Stripe Checkout
        return stripe.redirectToCheckout({ sessionId: data.sessionId });
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage(error.message, 'danger');
        payBtn.disabled = false;
        payBtn.textContent = translations.payWithStripe || 'Pay with Stripe';
    });
});