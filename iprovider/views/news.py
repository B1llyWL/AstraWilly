"""Новости и акции"""
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q
from django.utils.translation import gettext as _

from iprovider.models import News, Stocks, Country, City

def is_news_visible(news, country_id,city_id):
    """Проверяет, должна ли новость показываться при выбранной локации"""
    #Глобальная новость
    if not news.countries.exists() and not news.cities.exists():
        return True
    if city_id:
        #Новость с этим городом
        if news.cities.filter(id=city_id).exists():
            return True
        #Новость со страной этого города (и без городов)
        city = City.objects.filter(id=city_id).first()
        if city and not  news.cities.exists() and news.countries.filter(id=city.country_id).exists():
            return  True
    elif country_id:
        # Новость с этой страной и без городов
        if not  news.cities.exists() and news.countries.filter(id=country_id).exists():
            return  True
    return False

class NewsListView(ListView):
    """Список всех новостей"""
    model = News
    template_name = 'iprovider/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        # Опубликованные
        qs = News.objects.filter(is_published=True)

        # Получаем локацию из сессии
        country_id = self.request.session.get('selected_country_id')
        city_id = self.request.session.get('selected_city_id')

        # Пустой фильтр(Глобальные новости)
        q_filter = Q(countries__isnull=True, cities__isnull=True)

        if city_id:
            #1. Новости, у которых в городах есть этот город
            q_filter |=Q(cities__id=city_id)
            #2. Новости, у которых в странах есть страна этого города
            city = City.objects.filter(id=city_id).first()
            if city:
                q_filter |= Q(cities__isnull=True, countries__id=city.country_id)

        elif country_id:
            # Новости, у которых НЕТ cities, но страны включают эту страну
            q_filter |= Q(cities__isnull=True, countries__id=country_id)

            # Применяем фильтр, убираем дубли (distinct) из-за ManyToMany
        return  qs.filter(q_filter).distinct().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_country_id = self.request.session.get('selected_country_id')
        selected_city_id = self.request.session.get('selected_city_id')

        # Фильтрация новостей по географии
        news_filter = Q(countries__isnull=True, cities__isnull=True)

        if selected_city_id:
            news_filter |= Q(cities__id = selected_city_id)
            city_obj = City.objects.filter(id=selected_city_id).first()
            if city_obj:
                news_filter |=Q(cities__isnull = True, countries__id=city_obj.country_id)
        elif selected_country_id:
            news_filter |= Q(cities__isnull = True,countries__id = selected_country_id)

        latest_news = News.objects.filter(is_published = True) \
                                  .filter(news_filter) \
                                  .distinct() \
                                  .order_by('-created_at')[:3]
        news_for_template = []
        for news_item in latest_news:
            news_data = {
                'title': news_item.title,
                'date': news_item.created_at.strftime('%B %d, %Y'),
                'content': news_item.description[:150] + '...' if len(news_item.description) > 150 else news_item.description,
                'url':news_item.get_absolute_url()
                }
            if news_item.photo:
                    news_data['photo'] = news_item.photo
            news_for_template.append(news_data)

        context['news'] = news_for_template

        context.update({
            'title': 'AstraWilly - News',
            'company_name': 'AstraWilly',
            'news_count': self.get_queryset().count(),
            'countries': Country.objects.all(),
            'cities': City.objects.filter(country_id = selected_country_id) if selected_country_id else City.objects.none(),
            'selected_country':Country.objects.filter(id=self.request.session.get('selected_country_id')).first(),
            'selected_city': City.objects.filter(id=selected_city_id).first(),
        })
        return context


class NewsDetailView(DetailView):
    """Детальная страница новости"""
    model = News
    template_name = 'iprovider/news_detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        country_id =self.request.session.get('selected_country_id')
        city_id = self.request.session.get('selected_city_id')
        if not is_news_visible(obj, country_id,city_id):
            raise Http404("News not available in your location")
        return obj


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.object

        # Увеличиваем счетчик просмотров
        news.watched += 1
        news.save(update_fields=['watched'])

        country_id = self.request.session.get('selected_country_id')
        city_id = self.request.session.get('selected_city_id')

        all_visible = News.objects.filter(is_published = True)
        visible_pks = [n.pk for n in all_visible if is_news_visible(n, country_id, city_id)]

        visible_qs = News.objects.filter(pk__in=visible_pks).order_by('-created_at')

        try:
           current_index = list(visible_qs.values_list('pk', flat=True)).index(news.pk)
        except ValueError:
           current_index = -1

        prev_news = None
        next_news = None

        if current_index >0:
           prev_news = visible_qs[current_index -1]
        if current_index < len(visible_qs) -1:
           next_news =visible_qs[current_index +1]

        context.update({
           'title':f'AstraWilly - {news.title}',
           'company_name': 'AstraWilly',
           'next_news': next_news,
           'prev_news': prev_news,
        })
        return context

class StocksListView(ListView):
    """Список всех акций"""
    model = Stocks
    template_name = 'iprovider/stocks.html'
    context_object_name = 'stocks_list'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Stocks.objects.filter(is_published=True)
        country_id = self.request.session.get('selected_country_id')
        city_id=self.request.session.get('selected_city_id')

        #Глобальные акции (нет стран и городов)
        q_filter = Q(countries__isnull = True, cities__isnull = True)

        if city_id:
            q_filter |= Q(cities__id=city_id)
            city = City.objects.filter(id=city_id).first()
            if city:
                q_filter |= Q(cities__isnull=True, countries__id = city.country_id)
        elif country_id:
            q_filter |= Q(cities__isnull = True, countries__id = country_id)
        return  qs.filter(q_filter).distinct().order_by('-created_at')

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        selected_country_id = self.request.session.get('selected_country_id')
        selected_city_id = self.request.session.get('selected_city_id')

        # Общее количество отфильтрованных акций
        context['stocks_count'] = self.get_queryset().count()
        context['title'] = 'AstraWilly - Stocks'
        context['company_name'] = 'AstraWilly'
        context['countries'] = Country.objects.all()
        context['cities'] = City.objects.filter(country_id=selected_country_id) if selected_country_id else City.objects.none()
        context['selected_country'] =Country.objects.filter(id=selected_country_id).first()
        context['selected_city'] = City.objects.filter(id=selected_city_id).first()
        return context

class StocksDetailView(DetailView):
    """Детальная страница акции"""
    model = Stocks
    template_name = 'iprovider/stocks_detail.html'
    context_object_name = 'stock'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Stocks.objects.filter(is_published=True)

    def get_object(self, queryset = None):
        obj = super().get_object(queryset)
        country_id = self.request.session.get('selected_country_id')
        city_id = self.request.session.get('selected_city_id')
        if not  is_stocks_visible(obj,country_id,city_id):
            raise Http404(_("Stock not available in your location"))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object

        # Увеличиваем счетчик просмотров
        stock.watched += 1
        stock.save(update_fields=['watched'])

        country_id = self.request.session.get('selected_country_id')
        city_id = self.request.session.get('selected_city_id')

        # Навигация prev/next только по видимым акциям
        all_visible = Stocks.objects.filter(is_published=True)
        visible_pks = [s.pk for  s in all_visible if is_stocks_visible (s, country_id, city_id)]
        visible_qs = Stocks.objects.filter(pk__in=visible_pks).order_by('-created_at')

        try:
            current_index = list(visible_qs.values_list('pk', flat=True)).index(stock.pk)
        except ValueError:
            current_index = -1

        prev_stock = None
        next_stock = None
        if current_index >0:
            prev_stock = visible_qs[current_index -1]
        if current_index <len(visible_qs) -1:
            next_stock = visible_qs[current_index +1]

        context.update({
            'title':f'AstraWilly - {stock.title}',
            'company_name': 'AstraWilly',
            'next_stock':next_stock,
            'prev_stock':prev_stock,
        })
        return context

def is_stocks_visible(stock, country_id, city_id):
    """Проверяет, должна ли акция показываться при выбранной локации"""
    if not stock.countries.exists() and not stock.cities.exists():
        return True
    if city_id:
        if stock.cities.filter(id=city_id).exists():
            return True
        city = City.objects.filter(id=city_id).first()
        if city and not stock.cities.exists() and stock.countries.filter(id=city.country_id).exists():
            return True
    elif country_id:
        if not stock.cities.exists() and stock.countries.filter(id=country_id).exists():
            return  True
    return False