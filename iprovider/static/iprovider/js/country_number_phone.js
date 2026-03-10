document.addEventListener('DOMContentLoaded', function() {
    var phoneInputs = document.querySelectorAll('input[type="tel"], input[name="number"]');

    phoneInputs.forEach(function(input) {
        if (input && !input.dataset.itiInitialized) {
            var iti = window.intlTelInput(input, {
                separateDialCode: true,
                initialCountry: "ru",
                preferredCountries: ["ru", "de", "nl", "us", "kr", "jp", "mv"],
                utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js"
            });

            input.dataset.itiInitialized = "true";
            input.intlTelInputInstance = iti;

            var form = input.closest('form');
            if (form) {
                form.addEventListener('submit', function() {
                    if (iti.getNumber()) {
                        input.value = iti.getNumber();
                    }
                });
            }
        }
    });

    //Отображаемые номера телефонов с помощью флажков.
    var phoneDisplays = document.querySelectorAll('.phone-display');
    phoneDisplays.forEach(function(display) {
        var phoneNumber = display.textContent.trim();
        if (phoneNumber && phoneNumber !== '-') {
            var countryCode = getCountryCodeFromPhone(phoneNumber);
            if (countryCode) {
                var wrapper = document.createElement('div');
                wrapper.className = 'iti iti--separate-dial-code';
                wrapper.style.display = 'inline-block';
                wrapper.style.marginRight = '8px';

                var flagDiv = document.createElement('div');
                flagDiv.className = 'iti__flag iti__' + countryCode.toLowerCase();

                wrapper.appendChild(flagDiv);
                display.insertBefore(wrapper, display.firstChild);
            }
        }
    });
});

function getCountryCodeFromPhone(phoneNumber) {
    var cleaned = phoneNumber.replace(/[^\d+]/g, '');

    if (cleaned.startsWith('+7')) return 'ru';
    if (cleaned.startsWith('+1')) return 'us';
    if (cleaned.startsWith('+49')) return 'de';
    if (cleaned.startsWith('+31')) return 'nl';
    if (cleaned.startsWith('+82')) return 'kr';
    if (cleaned.startsWith('+81')) return 'jp';
    if (cleaned.startsWith('+960')) return 'mv';
    if (cleaned.startsWith('+44')) return 'gb';
    if (cleaned.startsWith('+33')) return 'fr';

    return 'ru';
}