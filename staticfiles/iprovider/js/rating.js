// rating.js
document.addEventListener('DOMContentLoaded', function() {
    const starRatings = document.querySelectorAll('.star-rating.interactive');

    starRatings.forEach(ratingContainer => {
        const stars = ratingContainer.querySelectorAll('i');
        const itemId = ratingContainer.dataset.id;
        const itemType = ratingContainer.dataset.type;

        // Загрузка текущего рейтинга пользователя
        loadUserRating(itemId, itemType, stars);

        // Обработка кликов по звездам
        stars.forEach(star => {
            star.addEventListener('click', function() {
                const ratingValue = this.dataset.value;
                submitRating(itemId, itemType, ratingValue, stars);
            });

            star.addEventListener('mouseover', function() {
                const hoverValue = this.dataset.value;
                highlightStars(stars, hoverValue);
            });

            star.addEventListener('mouseout', function() {
                const currentRating = getCurrentRating(stars);
                highlightStars(stars, currentRating);
            });
        });
    });

    function loadUserRating(itemId, itemType, stars) {
        // Загрузка рейтинга пользователя через AJAX
        fetch(`/api/get-rating/${itemType}/${itemId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.rating) {
                    highlightStars(stars, data.rating);
                }
                if (data.count) {
                    const countSpan = stars[0].closest('.star-rating').querySelector('.rating-count');
                    if (countSpan) {
                        countSpan.textContent = data.count;
                    }
                }
            })
            .catch(error => console.error('Error loading rating:', error));
    }

    function submitRating(itemId, itemType, ratingValue, stars) {
        const csrfToken = getCookie('csrftoken');

        fetch(`/api/set-rating/${itemType}/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                rating: ratingValue
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                highlightStars(stars, ratingValue);
                // Обновляем счетчик оценок
                const countSpan = stars[0].closest('.star-rating').querySelector('.rating-count');
                if (countSpan) {
                    countSpan.textContent = data.count;
                }
            }
        })
        .catch(error => console.error('Error submitting rating:', error));
    }

    function highlightStars(stars, rating) {
        stars.forEach(star => {
            star.classList.remove('bi-star-fill', 'bi-star-half', 'bi-star');
            if (star.dataset.value <= rating) {
                star.classList.add('bi-star-fill');
            } else {
                star.classList.add('bi-star');
            }
        });
    }

    function getCurrentRating(stars) {
        for (let i = stars.length - 1; i >= 0; i--) {
            if (stars[i].classList.contains('bi-star-fill')) {
                return parseInt(stars[i].dataset.value);
            }
        }
        return 0;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});