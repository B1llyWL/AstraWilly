document.addEventListener('DOMContentLoaded', function() {
    // Функция определения типа карты по первым цифрам
    function detectCardType(number) {
        number = number.replace(/\s/g, '');
        console.log('Detecting card type for:', number);
        if (!number) return '';
        let type = '';
        if (/^4/.test(number)) type = 'visa';
        else if (/^5[1-5]/.test(number)) type = 'mastercard';
        else if (/^2/.test(number)) type = 'mir';
        else if (/^62/.test(number)) type = 'unionpay';
        else if (/^3[47]/.test(number)) type = 'amex';
        else if (/^6(?:011|5)/.test(number)) type = 'discover';
        else if (/^35(?:2[89]|[3-8][0-9])/.test(number)) type = 'jcb';
        else if (/^3(?:0[0-5]|[68][0-9])/.test(number)) type = 'diners';
        console.log('Detected type:', type);
        return type;
    }

    // Инициализация масок (Cleave.js должен быть подключен)
    if (typeof Cleave !== 'undefined') {
        var cardNumber = new Cleave('#card-number', {
            creditCard: true,
            onCreditCardTypeChanged: function(type) {
                var customType = detectCardType(document.getElementById('card-number').value);
                setCardIcon(customType || type);
            }
        });

        new Cleave('#card-expiry', {
            date: true,
            datePattern: ['m', 'y']
        });

        new Cleave('#card-cvv', {
            blocks: [3, 1],
            numericOnly: true
        });
    }

    // Функция установки иконки карты
    function setCardIcon(type) {
        var icon = document.getElementById('card-type-icon');
        if (!icon) return;
        icon.className = 'card-type-icon';
        if (type) {
            icon.classList.add(type.toLowerCase());
        }
    }

    // Дополнительный обработчик ввода для надёжного определения
    document.getElementById('card-number')?.addEventListener('input', function(e) {
        var num = e.target.value;
        var type = detectCardType(num);
        setCardIcon(type);
    });

    // Логика выбора страны и автоматической подстановки валюты
    const countrySelect = document.getElementById('country');
    const currencySelect = document.getElementById('currency');

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

    // Переключение шагов
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const backBtn = document.getElementById('back-to-step1');

    // Шаг 1: инициирование платежа
    const formStep1 = document.getElementById('payment-form-step1');
    if (formStep1) {
        formStep1.addEventListener('submit', function(e) {
            e.preventDefault();

            const amount = document.getElementById('amount').value;
            const currency = document.getElementById('currency').value;
            const cardNumber = document.getElementById('card-number').value.replace(/\s/g, '');
            const cardExpiry = document.getElementById('card-expiry').value;
            const cardCvv = document.getElementById('card-cvv').value;

            // Валидация
            if (!amount || amount <= 0) {
                alert(gettext('Enter valid amount'));
                return;
            }
            if (cardNumber.length < 15) {
                alert(gettext('Invalid card number'));
                return;
            }
            if (!cardExpiry.match(/^\d{2}\/\d{2}$/)) {
                alert(gettext('Invalid expiry date'));
                return;
            }
            if (cardCvv.length < 3) {
                alert(gettext('Invalid CVV'));
                return;
            }

            // Отправка AJAX
            fetch(createPaymentUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'action': 'initiate',
                    'amount': amount,
                    'currency': currency,
                    'card_number': cardNumber,
                    'card_expiry': cardExpiry,
                    'card_cvv': cardCvv,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else if (data.status === 'otp_required') {
                    step1.classList.add('hidden');
                    step2.classList.remove('hidden');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(gettext('Server error'));
            });
        });
    }

    // Шаг 2: подтверждение кода
    const formStep2 = document.getElementById('payment-form-step2');
    if (formStep2) {
        formStep2.addEventListener('submit', function(e) {
            e.preventDefault();

            const otp = document.getElementById('otp-code').value;
            if (!otp || otp.length !== 6) {
                alert(gettext('Enter 6-digit code'));
                return;
            }

            fetch(createPaymentUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    'action': 'confirm',
                    'otp_code': otp,
                })
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data && data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(gettext('Server error'));
            });
        });
    }

    // Кнопка "Назад" (сменить карту)
    if (backBtn) {
        backBtn.addEventListener('click', function() {
            step1.classList.remove('hidden');
            step2.classList.add('hidden');
            document.getElementById('otp-code').value = '';
        });
    }
});