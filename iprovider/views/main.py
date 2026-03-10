from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.cache import  cache
from iprovider.models import News, Tariff, Country, City, Separately, Packets, Vacancy, ConnectionRequest
from django.db.models import Q
from django.utils.translation import gettext as _

class HomePageView(TemplateView):
    """Главная страница компании"""
    template_name = 'iprovider/home.html'

    def get_context_data(self, **kwargs):
        """Добавляем контекстные данные для шаблона"""
        context = super().get_context_data(**kwargs)

        # Получаем выбранную страну и город из сессии
        selected_country_id = self.request.session.get('selected_country_id')
        selected_city_id = self.request.session.get('selected_city_id')

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

        # Фильтрация новостей по географии
        news_filter = Q(countries__isnull=True, cities__isnull = True)

        if selected_city_id:
            news_filter |= Q(cities__id = selected_city_id)
            city_obj = City.objects.filter(id=selected_city_id).first()
            if city_obj:
                news_filter |= Q(cities__isnull=True, countries__id=city_obj.country_id)
        elif selected_country_id:
            news_filter |= Q(cities__isnull = True, countries__id = selected_country_id)
        # Получаем последние 3 опубликованные новости
        latest_news = News.objects.filter(is_published=True) \
                                  .filter(news_filter) \
                                  .distinct() \
                                  .order_by('-created_at')[:3]

        # Преобразуем в формат для шаблона
        news_for_template = []
        for news_item in latest_news:
            news_data = {
                'title': news_item.title,
                'date': news_item.created_at.strftime('%B %d, %Y'),
                'content': news_item.description[:150] + '...' if len(
                    news_item.description) > 150 else news_item.description,
                'url': news_item.get_absolute_url()
            }
            if news_item.photo:
                news_data['photo'] = news_item.photo
            news_for_template.append(news_data)

        # Фильтруем города по выбранной стране
        cities = City.objects.all()
        if selected_country:
            cities = cities.filter(country=selected_country)

        context.update({
            'title': 'AstraWilly - Home',
            'company_name': 'AstraWilly',
            'biography': {
                'year_founded': 2011,
                'founder': 'Wilchelm Walker von Lawrence',
                'description': _('AstraWilly is the largest provider and the undisputed leader of the telecommunications services market with the largest subscriber base and technical network coverage. The official website with the details of the company: www.astrawilly.com . Every year, more than 4 million people become new customers.')
            },
            'achievements': [
                _('More than 50,000 satisfied customers'),
                _('Internet speed up to 1 Gbit/s'),
                _('The best provider of the Year 2024'),
                _('24/7 technical support')

            ],
            'news': news_for_template,
            'selected_country': selected_country,
            'selected_city': selected_city,
            'countries': Country.objects.all(),
            'cities': cities
        })
        return context


def services(request):
    """Страница с сервисами"""
    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')

    selected_country = None
    selected_city = None
    cities = City.objects.none()

    if selected_country_id:
        try:
            selected_country = Country.objects.get(id=selected_country_id)
            cities = City.objects.filter(country=selected_country).select_related('country')
        except Country.DoesNotExist:
            pass

    if selected_city_id:
        try:
            selected_city = City.objects.get(id=selected_city_id)
        except City.DoesNotExist:
            pass

    # Ключ кэша зависит от выбранной локации
    cache_key = f'services_data_{selected_country_id}_{selected_city_id}'
    cached_data = cache.get(cache_key)

    if cached_data is None:
        # Получаем данные из БД
        separately_services = list(Separately.objects.all())
        packets_services = list(Packets.objects.all())
        # Сохраняем в кэш на 15 минут
        cache.set(cache_key, {'separately_services': separately_services, 'packets_services': packets_services}, 900)
    else:
        separately_services = cached_data['separately_services']
        packets_services = cached_data['packets_services']

    # Данные, зависящие от пользователя (не кэшируются)
    active_separately_requests=set()
    active_packet_requests = set()
    if request.user.is_authenticated:
        active_separately_requests=set(
            ConnectionRequest.objects.filter(
                user=request.user,
                separately__isnull=False,
                status__in=['pending', 'in_progress','approved']
            ).values_list('separately_id',flat=True)
        )
        active_packet_requests = set(
            ConnectionRequest.objects.filter(
                user=request.user,
                packet__isnull=False,
                status__in=['pending', 'in_progress', 'approved']
            ).values_list('packet_id', flat=True)
        )
    context = {
        'title': 'AstraWilly - Services',
        'company_name': 'AstraWilly',
        'separately_services': separately_services,
        'packets_services': packets_services,
        'selected_country': selected_country,
        'selected_city': selected_city,
        'countries': Country.objects.all(),
        'cities': cities,
        'item_type_separately': 'separately',
        'item_type_packet': 'packet',
        'active_separately_requests': active_separately_requests,
        'active_packet_requests': active_packet_requests
    }
    return render(request, 'iprovider/services.html', context)


def tariffs(request):
    """Страница с тарифами"""
    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')

    selected_country = None
    selected_city = None
    cities = City.objects.none()

    if selected_country_id:
        try:
            selected_country = Country.objects.get(id=selected_country_id)
            cities = City.objects.filter(country=selected_country).select_related('country')
        except Country.DoesNotExist:
            pass

    if selected_city_id:
        try:
            selected_city = City.objects.get(id=selected_city_id)
        except City.DoesNotExist:
            pass

    cache_key = f'tariffs_data_{selected_country_id}_{selected_city_id}'
    cached_data = cache.get(cache_key)

    if cached_data is None:
        # Получаем все тарифы
        tariffs_list = Tariff.objects.all().select_related('category')

        # Разделяем по категориям
        moonwilly_tariffs = []
        sunwilly_tariffs = []

        for tariff in tariffs_list:
            # Проверяем категорию тарифа
            if tariff.category and tariff.category.slug == 'wi-fi':
                moonwilly_tariffs.append(tariff)
            elif tariff.category and tariff.category.slug == 'mobile-internet':
                sunwilly_tariffs.append(tariff)

        cached_data = {
            'moonwilly_tariffs': moonwilly_tariffs,
            'sunwilly_tariffs':sunwilly_tariffs,
        }
        cache.set(cache_key, cached_data, 900)
    else:
        moonwilly_tariffs = cached_data['moonwilly_tariffs']
        sunwilly_tariffs = cached_data['sunwilly_tariffs']

    # Запросы, зависящие от пользователя
    active_tariff_requests =set()
    if request.user.is_authenticated:
        active_tariff_requests = set(
            ConnectionRequest.objects.filter(
                user=request.user,
                tariff__isnull=False,
                status__in=['pending', 'in_progress', 'approved']
            ).values_list('tariff_id', flat=True)
        )
    context = {
        'title': 'AstraWilly - Tariffs',
        'company_name': 'AstraWilly',
        'moonwilly_tariffs': moonwilly_tariffs,
        'sunwilly_tariffs': sunwilly_tariffs,
        'selected_country': selected_country,
        'selected_city': selected_city,
        'countries': Country.objects.all(),
        'cities': cities,
        'item_type':'tariff',
        'active_tariff_requests': active_tariff_requests,
    }
    return render(request, 'iprovider/tariffs.html', context)

def set_location(request):
    """Установка выбранной страны и города"""
    if request.method == 'POST':
        country_id = request.POST.get('country')
        city_id = request.POST.get('city')

        # Для отладки
        print(f"Устанавливаем локацию: country_id={country_id}, city_id={city_id}")

        if country_id:
            try:
                request.session['selected_country_id'] = int(country_id)
                messages.success(request, 'Location updated successfully!')
                print(f"Установлена страна ID: {country_id}")
            except (ValueError, TypeError):
                messages.error(request, 'Invalid country selected.')
                print(f"Ошибка при установке страны: {country_id}")
        else:
            request.session.pop('selected_country_id', None)
            print("Страна не выбрана, удаляем из сессии")

        if city_id:
            try:
                request.session['selected_city_id'] = int(city_id)
                print(f"Установлен город ID: {city_id}")
            except (ValueError, TypeError):
                messages.error(request, 'Invalid city selected.')
                print(f"Ошибка при установке города: {city_id}")
        else:
            request.session.pop('selected_city_id', None)
            print("Город не выбран, удаляем из сессии")

        request.session.modified = True

        print(f"Сессия после установки: {dict(request.session)}")

        # Для AJAX запросов
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})

        # Возвращаем на предыдущую страницу
        return_url = request.META.get('HTTP_REFERER', '/')
        return redirect(return_url)

    return redirect('home')


def get_cities(request):
    """API endpoint для получения городов по стране"""
    country_id = request.GET.get('country_id')
    if country_id:
        cities = City.objects.filter(country_id=country_id).select_related('country').order_by('name')
        cities_data = [
            {
                'id': city.id,
                'name': city.name,
                'country_name': city.country.name
            }
            for city in cities
        ]
        print(f"Получены города для страны {country_id}: {len(cities_data)} городов")
        return JsonResponse({'cities': cities_data})

    print("Получен запрос на города без ID страны")
    return JsonResponse({'cities': []})

def find_location(request):
    """
    API endpoint для определения ID страны и города по их названиям.
    Используется для автоматической установки локации после геокодинга.
    """
    country_name = request.GET.get('country')
    city_name = request.GET.get('city')

    result = {'country_id': None,'city_id': None}

    if country_name:
        # Ищем страну без учета регистра
        country = Country.objects.filter(name__iexact=country_name).first()
        if country:
            result['country_id'] = country.id
            if city_name:
                city = City.objects.filter(country=country, name__iexact=city_name).first()
                if city:
                    result['city_id'] = city.id
    return JsonResponse(result)

def support(request):
    """Страница поддержки"""
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

    context = {
        'title': 'AstraWilly - Support',
        'company_name': 'AstraWilly',
        'selected_country': selected_country,
        'selected_city': selected_city,
        'countries': Country.objects.all(),
    }
    return render(request, 'iprovider/support.html', context)

def vacancy_view(request):
    """Страница вакансий"""
    # Получаем выбранную локацию из сессии
    selected_country_id = request.session.get('selected_country_id')
    selected_city_id = request.session.get('selected_city_id')

    # Для отладки
    print(f"\n=== VACANCY VIEW ===")
    print(f"Selected country ID from session: {selected_country_id}")
    print(f"Selected city ID from session: {selected_city_id}")

    # Начинаем с опубликованных вакансий
    vacancies = Vacancy.objects.filter(is_published=True).prefetch_related(
         'countries', 'category', 'locations__place__country', 'locations__place__city', 'locations__languages'
    ).distinct()

    print(f"Всего опубликованных вакансий: {vacancies.count()}")

    # Если выбрана страна
    if selected_country_id:
        print(f"Фильтруем по стране ID: {selected_country_id}")

        try:
            # Фильтруем вакансии несколькими способами
            vacancies = vacancies.filter(
                Q(countries__id=selected_country_id) |
                Q(locations__place__country__id=selected_country_id)
            ).distinct()

            print(f"Вакансий после фильтрации по стране: {vacancies.count()}")

            # Если выбран город
            if selected_city_id:
                print(f"Фильтруем по городу ID: {selected_city_id}")

                # Фильтруем вакансии по городу
                vacancies = vacancies.filter(
                    Q(locations__place__city__id=selected_city_id)
                ).distinct()

                print(f"Вакансий после фильтрации по городу: {vacancies.count()}")
        except Exception as e:
            print(f"Ошибка при фильтрации: {e}")
    else:
        print("Страна не выбрана, показываем все вакансии")

    # Для отладки выведем все вакансии
    print(f"\n=== ВАКАНСИИ ===")
    for vacancy in vacancies:
        print(f"Вакансия: {vacancy.title}")
        print(f"  Страны: {[c.name for c in vacancy.countries.all()]}")
        print(f"  Локации:")
        for location in vacancy.locations.all():
            place = location.place
            print(f"-{place.address or place.name}, "
                  f"Город: {place.city.name if place.city else '-'}, "
                  f"Страна: {place.country.name if place.country else '-'}, "
                  f"Языки: {[lang.name for lang in location.languages.all()]}")

    print(f"=== КОНЕЦ ВАКАНСИЙ ===\n")

    # Получаем страны и города для выпадающих списков
    countries = Country.objects.all()

    # Если выбрана страна, фильтруем города
    if selected_country_id:
        cities = City.objects.filter(country_id=selected_country_id)
    else:
        cities = City.objects.all()

    active_vacancy_requests = set()
    if request.user.is_authenticated:
        active_vacancy_requests=set(
            ConnectionRequest.objects.filter(
                user=request.user,
                vacancy__isnull=False,
                status__in=['pending', 'in_progress', 'approved']
            ).values_list('vacancy_id', flat=True)
        )

    context = {
        'vacancies': vacancies,
        'countries': countries,
        'cities': cities,
        'selected_country': Country.objects.filter(id=selected_country_id).first(),
        'selected_city': City.objects.filter(id=selected_city_id).first(),
        'item_type': 'vacancy',
        'active_vacancy_requests': active_vacancy_requests,
    }
    return render(request, 'iprovider/vacancy.html', context)


def search(request):
    """Функция поиска"""
    query = request.GET.get('q', '')
    results = []

    if query:
        # Поиск по тарифам
        tariff_results = Tariff.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        # Поиск по новостям
        news_results = News.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            is_published=True
        )

        results = list(tariff_results) + list(news_results)

    context = {
        'query': query,
        'results': results,
        'results_count': len(results),
        'title': f'Search: {query}' if query else 'Search'
    }

    return render(request, 'iprovider/search_results.html', context)
