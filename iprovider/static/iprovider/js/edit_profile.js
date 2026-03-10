console.log('Checkboxes:', document.querySelectorAll('input[name="preferred_contact_methods"]').length);
console.log('Badges:', document.querySelectorAll('.preview-badges .badge').length);

document.addEventListener('DOMContentLoaded', function() {
    const methodCheckboxes = document.querySelectorAll('input[name="preferred_contact_methods"]');
    const badges = document.querySelectorAll('.preview-badges .badge');

    function updateBadges() {
        // Сначала все бейджи делаем серыми
        badges.forEach(b => {
            b.classList.remove('bg-success');
            b.classList.add('bg-secondary');
        });

        // Для каждого выбранного чекбокса находим соответствующий бейдж и делаем зелёным
        methodCheckboxes.forEach(cb => {
            if (cb.checked) {
                const badge = document.querySelector(`.preview-badges .badge[data-method="${cb.value}"]`);
                if (badge) {
                    badge.classList.remove('bg-secondary');
                    badge.classList.add('bg-success');
                }
            }
        });
    }

    // Инициализация при загрузке страницы
    updateBadges();

    // Следим за изменениями всех чекбоксов
    methodCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateBadges);
    });
});