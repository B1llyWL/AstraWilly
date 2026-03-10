from .models import Country, City
from django.core.cache import cache

def location_context(request):
    """Добавляет страны и города в контекст всех шаблонов"""
    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')

    selected_country = None
    selected_city = None

    if selected_country_id:
        try:
            selected_country = Country.objects.get(id=selected_country_id)
        except Country.DoesNotExist:
            pass

    if selected_city_id:
        try:
            selected_city = City.objects.get(id=selected_city_id)
        except City.DoesNotExist:
            pass

    # Кэшируем списки стран и городов на 24 часа
    countries = cache.get('all_countries')
    if not countries:
        countries = list(Country.objects.all())
        cache.set('all_countries', countries, 86400)

    cities = cache.get('all_cities')
    if not cities:
        cities = list(City.objects.all())
        cache.set('all_cities', cities, 86400)

    return {
        'selected_country': selected_country,
        'selected_city': selected_city,
        'countries': countries,
        'cities': cities,
    }