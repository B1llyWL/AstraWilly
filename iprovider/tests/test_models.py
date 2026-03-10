import pytest
from iprovider.models import Tariff,Category, Country, City, TariffPrice
@pytest.mark.django_db
def test_tariff_creation():
    """Тест создания тарифа с базовыми полями."""
    category = Category.objects.create(title="Test Category")
    tariff = Tariff.objects.create(
        title="Test Tariff",
        price=9.99,
        category=category
    )
    assert  tariff.title == "Test Tariff"
    assert tariff.price == 9.99
    assert  tariff.category == category
    # проверяем __str__
    assert str(tariff) == "Test Tariff"

@pytest.mark.django_db
def test_tariff_get_price_for_location():
    """Тест метода get_price_for_location для тарифа."""
    # Создаем страну и город
    country = Country.objects.create(name="Test Country")
    city = City.objects.create(name="Test City", country=country)
    category = Category.objects.create(title="Test Cat")
    tariff = Tariff.objects.create(title="Test", price=10.0, category=category)

    #Создаем специальную цену для города
    TariffPrice.objects.create(tariff=tariff,city=city, price=8.0)

    # Проверяем, что для города возвращается цена 8.0
    assert tariff.get_price_for_location(city=city) == 8.0
    assert  tariff.get_price_for_location() == 10.0

@pytest.mark.django_db
def test_country_creation():
    country = Country.objects.create(name="Germany", code="+49")
    assert country.name == "Germany"
    assert  country.code == "+49"
    assert str(country) == "Germany"

@pytest.mark.django_db
def test_city_creation():
    country = Country.objects.create(name="Germany")
    city = City.objects.create(name="Berlin", country=country)
    assert city.name == "Berlin"
    assert city.country == country
    assert  str(city) == "Berlin, Germany"