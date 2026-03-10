import pytest
from django.urls import reverse
from django.utils import translation
from iprovider.models import Tariff, Category, Country, City


@pytest.fixture(autouse=True)
def set_default_language():
    """Устанавливает английский язык перед каждым тестом."""
    translation.activate('en')


@pytest.mark.django_db
class TestHomeView:
    """Тесты главной страницы."""

    def test_home_view_status_code(self, client):
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 200

    def test_home_uses_correct_template(self, client):
        response = client.get(reverse('home'))
        assert 'iprovider/home.html' in [t.name for t in response.templates]

    def test_home_view_context(self, client):
        response = client.get(reverse('home'))
        assert 'countries' in response.context
        assert 'news' in response.context


@pytest.mark.django_db
class TestTariffsView:
    """Тесты страницы тарифов."""

    @pytest.fixture
    def create_tariffs(self):
        cat1 = Category.objects.create(title="Wi-Fi", slug="wi-fi")
        cat2 = Category.objects.create(title="Mobile Internet", slug="mobile-internet")
        Tariff.objects.create(title="Tariff A", price=10.0, category=cat1)
        Tariff.objects.create(title="Tariff B", price=20.0, category=cat2)
        return cat1, cat2

    def test_tariffs_view_status_code(self, client, create_tariffs):
        url = reverse('tariffs')
        response = client.get(url)
        assert response.status_code == 200

    def test_tariffs_view_uses_correct_template(self, client):
        response = client.get(reverse('tariffs'))
        assert 'iprovider/tariffs.html' in [t.name for t in response.templates]

    def test_tariffs_view_context_has_tariffs(self, client, create_tariffs):
        response = client.get(reverse('tariffs'))
        assert 'moonwilly_tariffs' in response.context
        assert 'sunwilly_tariffs' in response.context


@pytest.mark.django_db
class TestServicesView:
    """Тесты страницы услуг."""

    def test_services_view_status_code(self, client):
        url = reverse('services')
        response = client.get(url)
        assert response.status_code == 200

    def test_services_view_uses_correct_template(self, client):
        response = client.get(reverse('services'))
        assert 'iprovider/services.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestVacancyView:
    """Тесты страницы вакансий."""

    def test_vacancy_view_status_code(self, client):
        url = reverse('vacancy')
        response = client.get(url)
        assert response.status_code == 200

    def test_vacancy_view_uses_correct_template(self, client):
        response = client.get(reverse('vacancy'))
        assert 'iprovider/vacancy.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestSupportView:
    """Тесты страницы поддержки"""

    def test_support_view_status_code(self, client):
        url = reverse('support')
        response = client.get(url)
        assert response.status_code == 200

    def test_support_view_uses_correct_template(self, client):
        response = client.get(reverse('support'))
        assert 'iprovider/support.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestSetLocation:
    """Тесты для функции set_location (AJAX и POST)."""

    def test_set_location_post(self, client):
        # Создадим страну
        country = Country.objects.create(name="Test Country")
        url = reverse('set_location')
        response = client.post(url, {'country': country.id, 'city': ''})
        # Должен быть редирект (302)
        assert response.status_code == 302
        # Проверка на появление страны
        session = client.session
        assert session.get('selected_country_id') == country.id

    def test_set_location_ajax(self, client):
        country = Country.objects.create(name="Test Country")
        url = reverse('set_location')
        response = client.post(
            url,
            {'country': country.id, 'city': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        assert response.status_code == 200
        assert response.json() == {'status': 'success'}


@pytest.mark.django_db
class TestGetCities:
    """Тесты для API получения городов."""

    def test_get_cities_with_country(self, client):
        country = Country.objects.create(name="Test Country")
        city = City.objects.create(name="Test City", country=country)
        url = reverse('get_cities')
        response = client.get(url, {'country_id': country.id})
        assert response.status_code == 200
        data = response.json()
        assert 'cities' in data
        assert len(data['cities']) == 1
        assert data['cities'][0]['name'] == city.name

    def test_get_cities_without_country(self, client):
        url = reverse('get_cities')
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['cities'] == []