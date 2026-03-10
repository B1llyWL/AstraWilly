from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
import random
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class TranslationMixin(models.Model):
    """Миксин для получения переводов в зависимости от текущего языка"""

    class Meta:
        abstract = True

    def get_translated_field(self, field_name):
        """Получает поле для текущего языка"""
        lang = get_language()[:2] if get_language() else 'en'

        translated_field = f'{field_name}_{lang}'
        if hasattr(self, translated_field):
            value = getattr(self, translated_field)
            if value:
                return value

        # Fallback на основное поле
        return getattr(self, field_name, '')

    @property
    def current_language(self):
        """Возвращает текущий язык (en, de, nl, ru, uk)"""
        lang = get_language()[:2] if get_language() else 'en'
        return lang if lang in ['en', 'de', 'nl', 'ru', 'uk'] else 'en'

class Country(TranslationMixin):
    name = models.CharField(max_length=100, verbose_name=_('Country'), unique=True)
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Name (EN)")
    name_de = models.CharField(max_length=100, blank=True, verbose_name="Name (DE)")
    name_nl = models.CharField(max_length=100, blank=True, verbose_name="Name (NL)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Name (RU)")
    name_uk = models.CharField(max_length=100, blank=True, verbose_name="Name (UK)")

    code = models.CharField(max_length=10, verbose_name=_('Country code'), blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD', verbose_name=_('Currency code'))

    def __str__(self):
        return self.get_translated_field('name')

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    @property
    def current_name(self):
        return self.get_translated_field('name')

class City(TranslationMixin):
    name = models.CharField(max_length=100, verbose_name=_('City'))
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Name (EN)")
    name_de = models.CharField(max_length=100, blank=True, verbose_name="Name (DE)")
    name_nl = models.CharField(max_length=100, blank=True, verbose_name="Name (NL)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Name (RU)")
    name_uk = models.CharField(max_length=100, blank=True, verbose_name="Name (UK)")

    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Country'))

    def __str__(self):
        return f"{self.get_translated_field('name')}, {self.country.name}"

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        unique_together = ['name', 'country']

    @property
    def current_name(self):
        return self.get_translated_field('name')

class Category(TranslationMixin):
    title = models.CharField(max_length=150, verbose_name=_('Category name'))
    title_en = models.CharField(max_length=150, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=150, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=150, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=150, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=150, blank=True, verbose_name="Title (UK)")

    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name=_('Parent category'), related_name='subcategories')

    def __str__(self):
        return self.get_translated_field('title')

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Language(TranslationMixin):
    name = models.CharField(max_length=100, verbose_name=_('Language'), unique=True)
    name_en = models.CharField(max_length=100, blank=True, verbose_name="Name (EN)")
    name_de = models.CharField(max_length=100, blank=True, verbose_name="Name (DE)")
    name_nl = models.CharField(max_length=100, blank=True, verbose_name="Name (NL)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name="Name (RU)")
    name_uk = models.CharField(max_length=100, blank=True, verbose_name="Name (UK)")

    def __str__(self):
        return self.get_translated_field('name')

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')

    @property
    def current_name(self):
        return self.get_translated_field('name')

class Place(TranslationMixin):
    name = models.CharField(max_length=255, verbose_name=_('Place name'), blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, verbose_name="Name (EN)")
    name_de = models.CharField(max_length=255, blank=True, verbose_name="Name (DE)")
    name_nl = models.CharField(max_length=255, blank=True, verbose_name="Name (NL)")
    name_ru = models.CharField(max_length=255, blank=True, verbose_name="Name (RU)")
    name_uk = models.CharField(max_length=255, blank=True, verbose_name="Name (UK)")

    address = models.TextField(verbose_name=_('Full address'), blank=True, null=True)
    address_en = models.TextField(blank=True, verbose_name="Address (EN)")
    address_de = models.TextField(blank=True, verbose_name="Address (DE)")
    address_nl = models.TextField(blank=True, verbose_name="Address (NL)")
    address_ru = models.TextField(blank=True, verbose_name="Address (RU)")
    address_uk = models.TextField(blank=True, verbose_name="Address (UK)")

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name=_('Country'), null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, verbose_name=_('City'), null=True, blank=True)

    def save(self, *args, **kwargs):
        # Если адрес указан, но имя отсутствует, используйте адрес вместо имени
        if self.address and not self.name:
            self.name = self.address

        # Автоматическая установка страны на основе ключевых слов в адресе
        if self.address and not self.country:
            address_lower = self.address.lower()
            if 'russia' in address_lower or 'россия' in address_lower:
                country, _ = Country.objects.get_or_create(name='Russia')
                self.country = country
            elif 'usa' in address_lower or 'сша' in address_lower or 'america' in address_lower:
                country, _ = Country.objects.get_or_create(name='USA')
                self.country = country
            elif 'germany' in address_lower or 'германия' in address_lower:
                country, _ = Country.objects.get_or_create(name='Germany')
                self.country = country
            elif 'france' in address_lower or 'франция' in address_lower:
                country, _ = Country.objects.get_or_create(name='France')
                self.country = country
            elif 'uk' in address_lower or 'великобритания' in address_lower or 'england' in address_lower:
                country, _ = Country.objects.get_or_create(name='United Kingdom')
                self.country = country
        super().save(*args, **kwargs)

    def __str__(self):
        if self.city and self.country:
            return f"{self.get_translated_field('address')} ({self.city.name}, {self.country.name})"
        elif self.country:
            return f"{self.get_translated_field('address')} ({self.country.name})"
        else:
            return self.get_translated_field('address')

    class Meta:
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')

    @property
    def current_name(self):
        return self.get_translated_field('name')

    @property
    def current_address(self):
        return self.get_translated_field('address')

class VacancyLocation(models.Model):
    """Связь между вакансией и конкретным офисом с требуемыми языковыми навыками."""
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, verbose_name=_('Vacancy'),
                                related_name='locations')
    place = models.ForeignKey('Place', on_delete=models.CASCADE, verbose_name=_('Office'))
    languages = models.ManyToManyField('Language', verbose_name=_('Required languages'))

    class Meta:
        verbose_name = _('Vacancy office')
        verbose_name_plural = _('Vacancy offices')
        unique_together = ['vacancy', 'place']

    def __str__(self):
        return f"{self.vacancy.title} - {self.place}"

class Vacancy(TranslationMixin):
    title = models.CharField(max_length=255, verbose_name=_('Vacancy title'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=255, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=255, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=255, blank=True, verbose_name="Title (UK)")

    price = models.FloatField(verbose_name=_('Base price ($)'))
    countries = models.ManyToManyField(Country, verbose_name=_('Countries'), blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    description = models.TextField(default='Description will be here soon', verbose_name=_('Description'))
    description_en = models.TextField(blank=True, default='', verbose_name="Description (EN)")
    description_de = models.TextField(blank=True, default='', verbose_name="Description (DE)")
    description_nl = models.TextField(blank=True, default='', verbose_name="Description (NL)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Description (RU)")
    description_uk = models.TextField(blank=True, default='', verbose_name="Description (UK)")

    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    watched = models.IntegerField(default=0, verbose_name=_('Views'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='vacancy')
    slug = models.SlugField(unique=True, null=True)

    # Simplified features field
    features_text = models.TextField(
        blank=True,
        verbose_name=_('Features (text)'),
        help_text=_('Each feature on a new line. Will be displayed as a list.')
    )
    features_text_en = models.TextField(blank=True, default='', verbose_name="Features (EN)")
    features_text_de = models.TextField(blank=True, default='', verbose_name="Features (DE)")
    features_text_nl = models.TextField(blank=True, default='', verbose_name="Features (NL)")
    features_text_ru = models.TextField(blank=True, default='', verbose_name="Features (RU)")
    features_text_uk = models.TextField(blank=True, default='', verbose_name="Features (UK)")

    details_html = models.TextField(
        blank=True,
        verbose_name=_('Detailed description(HTML)'),
        help_text=_('Use HTML tags for formatting (e.g., <ul>, <li>, <strong>.)')
    )
    details_html_en = models.TextField(blank=True, default='', verbose_name="Details HTML (EN)")
    details_html_de = models.TextField(blank=True, default='', verbose_name="Details HTML (DE)")
    details_html_nl = models.TextField(blank=True, default='', verbose_name="Details HTML (NL)")
    details_html_ru = models.TextField(blank=True, default='', verbose_name="Details HTML (RU)")
    details_html_uk = models.TextField(blank=True, default='', verbose_name="Details HTML (UK)")

    def get_absolute_url(self):
        return reverse('vacancy_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.get_translated_field('title')

    def get_features_list(self):
        """Возвращает список функций"""
        features_text = self.get_translated_field('features_text')
        if features_text:
            lines = features_text.strip().split('\n')
            features = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    features.append(line[1:].strip())
                elif ' - ' in line:
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        features.append(parts[1].strip())
                    else:
                        features.append(line)
                else:
                    features.append(line)
            return features if features else [self.get_translated_field('description')]
        return [self.get_translated_field('description')] if self.get_translated_field('description') else [
            _("No features")]

    def display_features(self):
        """Функции отображения для администратора"""
        features = self.get_features_list()
        if features:
            html = '<ul style="margin: 0; padding-left: 20px;">'
            for feature in features[:5]:
                html += f'<li>{feature}</li>'
            if len(features) > 5:
                html += f'<li>... and {len(features) - 5} more</li>'
            html += '</ul>'
            return mark_safe(html)
        return mark_safe('<span style="color: #999;">—</span>')

    display_features.short_description = _('Features')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновление стран на основе связанных офисов
        country_ids = self.locations.values_list('place__country_id', flat=True).distinct()
        if country_ids:
            self.countries.set(Country.objects.filter(id__in=country_ids))
        else:
            self.countries.clear()

    class Meta:
        verbose_name = _('Vacancy')
        verbose_name_plural = _('Vacancies')

    @property
    def current_title(self):
        return self.get_translated_field('title')

    @property
    def current_description(self):
        return self.get_translated_field('description')

    @property
    def current_details_html(self):
        return self.get_translated_field('details_html')

class Tariff(TranslationMixin):
    title = models.CharField(max_length=255, verbose_name=_('Tariff name'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=255, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=255, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=255, blank=True, verbose_name="Title (UK)")

    price = models.FloatField(verbose_name=_('Base price ($)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    watched = models.IntegerField(default=0, verbose_name=_('Views'))

    description = models.TextField(default='Description will be here soon', verbose_name=_('Description'))
    description_en = models.TextField(blank=True, default='', verbose_name="Description (EN)")
    description_de = models.TextField(blank=True, default='', verbose_name="Description (DE)")
    description_nl = models.TextField(blank=True, default='', verbose_name="Description (NL)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Description (RU)")
    description_uk = models.TextField(blank=True, default='', verbose_name="Description (UK)")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='tariff_categories')
    slug = models.SlugField(unique=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name=_('Display order'))

    features_text = models.TextField(
        blank=True,
        verbose_name=_('Features (text)'),
        help_text=_('Each feature on a new line. Will be displayed as a list.')
    )
    features_text_en = models.TextField(blank=True, default='', verbose_name="Features (EN)")
    features_text_de = models.TextField(blank=True, default='', verbose_name="Features (DE)")
    features_text_nl = models.TextField(blank=True, default='', verbose_name="Features (NL)")
    features_text_ru = models.TextField(blank=True, default='', verbose_name="Features (RU)")
    features_text_uk = models.TextField(blank=True, default='', verbose_name="Features (UK)")

    @property
    def current_price(self):
        return self.price

    def __str__(self):
        return self.get_translated_field('title')

    def get_price_for_location(self, country=None, city=None):
        """Get price for specific location"""
        if city:
            city_price = TariffPrice.objects.filter(tariff=self, city=city).first()
            if city_price:
                return city_price.price
        if country:
            country_price = TariffPrice.objects.filter(tariff=self, country=country).first()
            if country_price:
                return country_price.price
        return self.price

    def get_features_list(self):
        """Возвращает список функций"""
        features_text = self.get_translated_field('features_text')
        if features_text:
            lines = features_text.strip().split('\n')
            features = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    features.append(line[1:].strip())
                elif ' - ' in line:
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        features.append(parts[1].strip())
                    else:
                        features.append(line)
                else:
                    features.append(line)
            return features if features else [self.get_translated_field('description')]
        if self.get_translated_field('description'):
            return [self.get_translated_field('description')]
        return [_("No features")]

    def display_features(self):
        """Функции отображения для администратора"""
        features = self.get_features_list()
        if features:
            html = '<ul style="margin: 0; padding-left: 20px;">'
            for feature in features[:5]:
                html += f'<li>{feature}</li>'
            if len(features) > 5:
                html += f'<li>... and {len(features) - 5} more</li>'
            html += '</ul>'
            return mark_safe(html)
        return mark_safe('<span style="color: #999;">—</span>')

    display_features.short_description = _('Features')

    class Meta:
        verbose_name = _('Tariff')
        verbose_name_plural = _('Tariffs')
        ordering = ['order', 'title']

class TariffPrice(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name='tariff_prices')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Country'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('City'))
    price = models.FloatField(verbose_name=_('Price ($)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Tariff price')
        verbose_name_plural = _('Tariff prices')
        unique_together = [
            ['tariff', 'country'],
            ['tariff', 'city']
        ]

    def clean(self):
        if not self.country and not self.city:
            raise ValidationError(_('You must specify either a country or a city.'))
        if self.country and self.city:
            raise ValidationError(_('Please indicate only the country OR only the city.'))

    def __str__(self):
        if self.city:
            return f"{self.tariff.title} - {self.city.name}: ${self.price}"
        elif self.country:
            return f"{self.tariff.title} - {self.country.name}: ${self.price}"
        return f"{self.tariff.title}: ${self.price}"

class Separately(TranslationMixin):
    title = models.CharField(max_length=255, verbose_name=_('Separate service name'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=255, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=255, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=255, blank=True, verbose_name="Title (UK)")

    price = models.FloatField(verbose_name=_('Base price ($)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    watched = models.IntegerField(default=0, verbose_name=_('Views'))

    description = models.TextField(default='Description will be here soon', verbose_name=_('Description'))
    description_en = models.TextField(blank=True, default='', verbose_name="Description (EN)")
    description_de = models.TextField(blank=True, default='', verbose_name="Description (DE)")
    description_nl = models.TextField(blank=True, default='', verbose_name="Description (NL)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Description (RU)")
    description_uk = models.TextField(blank=True, default='', verbose_name="Description (UK)")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='separately_categories')
    slug = models.SlugField(unique=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name=_('Display order'))

    features_text = models.TextField(
        blank=True,
        verbose_name=_('Features (text)'),
        help_text=_('Each feature on a new line. Will be displayed as a list.')
    )
    features_text_en = models.TextField(blank=True, default='', verbose_name="Features (EN)")
    features_text_de = models.TextField(blank=True, default='', verbose_name="Features (DE)")
    features_text_nl = models.TextField(blank=True, default='', verbose_name="Features (NL)")
    features_text_ru = models.TextField(blank=True, default='', verbose_name="Features (RU)")
    features_text_uk = models.TextField(blank=True, default='', verbose_name="Features (UK)")

    @property
    def current_price(self):
        return self.price

    def __str__(self):
        return self.get_translated_field('title')

    def get_price_for_location(self, country=None, city=None):
        if city:
            city_price = SeparatelyPrice.objects.filter(separately=self, city=city).first()
            if city_price:
                return city_price.price
        if country:
            country_price = SeparatelyPrice.objects.filter(separately=self, country=country).first()
            if country_price:
                return country_price.price
        return self.price

    def get_features_list(self):
        features_text = self.get_translated_field('features_text')
        if features_text:
            lines = features_text.strip().split('\n')
            features = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    features.append(line[1:].strip())
                elif ' - ' in line:
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        features.append(parts[1].strip())
                    else:
                        features.append(line)
                else:
                    features.append(line)
            return features if features else [self.get_translated_field('description')]
        if self.get_translated_field('description'):
            return [self.get_translated_field('description')]
        return [_("No features")]

    def display_features(self):
        features = self.get_features_list()
        if features:
            html = '<ul style="margin: 0; padding-left: 20px;">'
            for feature in features[:5]:
                html += f'<li>{feature}</li>'
            if len(features) > 5:
                html += f'<li>... and {len(features) - 5} more</li>'
            html += '</ul>'
            return mark_safe(html)
        return mark_safe('<span style="color: #999;">—</span>')

    display_features.short_description = _('Features')

    class Meta:
        verbose_name = _('Separate service')
        verbose_name_plural = _('Separate services')
        ordering = ['order', 'title']


class SeparatelyPrice(models.Model):
    separately = models.ForeignKey(Separately, on_delete=models.CASCADE, related_name='separately_prices')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Country'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('City'))
    price = models.FloatField(verbose_name=_('Price ($)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Separate service price')
        verbose_name_plural = _('Separate service prices')
        unique_together = [
            ['separately', 'country'],
            ['separately', 'city']
        ]

    def clean(self):
        if not self.country and not self.city:
            raise ValidationError(_('You must specify either a country or a city.'))
        if self.country and self.city:
            raise ValidationError(_('Please indicate only the country OR only the city.'))

    def __str__(self):
        if self.city:
            return f"{self.separately.title} - {self.city.name}: ${self.price}"
        elif self.country:
            return f"{self.separately.title} - {self.country.name}: ${self.price}"
        return f"{self.separately.title}: ${self.price}"

class Packets(TranslationMixin):
    title = models.CharField(max_length=255, verbose_name=_('Packet name'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=255, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=255, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=255, blank=True, verbose_name="Title (UK)")

    price = models.FloatField(verbose_name=_('Base price ($)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    watched = models.IntegerField(default=0, verbose_name=_('Views'))

    description = models.TextField(default='Description will be here soon', verbose_name=_('Description'))
    description_en = models.TextField(blank=True, default='', verbose_name="Description (EN)")
    description_de = models.TextField(blank=True, default='', verbose_name="Description (DE)")
    description_nl = models.TextField(blank=True, default='', verbose_name="Description (NL)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Description (RU)")
    description_uk = models.TextField(blank=True, default='', verbose_name="Description (UK)")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='packets_categories')
    slug = models.SlugField(unique=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name=_('Display order'))

    features_text = models.TextField(
        blank=True,
        verbose_name=_('Features (text)'),
        help_text=_('Each feature on a new line. Will be displayed as a list.')
    )
    features_text_en = models.TextField(blank=True, default='', verbose_name="Features (EN)")
    features_text_de = models.TextField(blank=True, default='', verbose_name="Features (DE)")
    features_text_nl = models.TextField(blank=True, default='', verbose_name="Features (NL)")
    features_text_ru = models.TextField(blank=True, default='', verbose_name="Features (RU)")
    features_text_uk = models.TextField(blank=True, default='', verbose_name="Features (UK)")

    @property
    def current_price(self):
        return self.price

    def __str__(self):
        return self.get_translated_field('title')

    def get_price_for_location(self, country=None, city=None):
        if city:
            city_price = PacketsPrice.objects.filter(packets=self, city=city).first()
            if city_price:
                return city_price.price
        if country:
            country_price = PacketsPrice.objects.filter(packets=self, country=country).first()
            if country_price:
                return country_price.price
        return self.price

    def get_features_list(self):
        features_text = self.get_translated_field('features_text')
        if features_text:
            lines = features_text.strip().split('\n')
            features = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    features.append(line[1:].strip())
                elif ' - ' in line:
                    parts = line.split(' - ', 1)
                    if len(parts) == 2:
                        features.append(parts[1].strip())
                    else:
                        features.append(line)
                else:
                    features.append(line)
            return features if features else [self.get_translated_field('description')]
        if self.get_translated_field('description'):
            return [self.get_translated_field('description')]
        return [_("No features")]

    def display_features(self):
        features = self.get_features_list()
        if features:
            html = '<ul style="margin: 0; padding-left: 20px;">'
            for feature in features[:5]:
                html += f'<li>{feature}</li>'
            if len(features) > 5:
                html += f'<li>... and {len(features) - 5} more</li>'
            html += '</ul>'
            return mark_safe(html)
        return mark_safe('<span style="color: #999;">—</span>')

    display_features.short_description = _('Features')

    class Meta:
        verbose_name = _('Packet')
        verbose_name_plural = _('Packets')
        ordering = ['order', 'title']


class PacketsPrice(models.Model):
    packets = models.ForeignKey(Packets, on_delete=models.CASCADE, related_name='packets_prices')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Country'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('City'))
    price = models.FloatField(verbose_name=_('Price ($)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Packet price')
        verbose_name_plural = _('Packet prices')
        unique_together = [
            ['packets', 'country'],
            ['packets', 'city']
        ]

    def clean(self):
        if not self.country and not self.city:
            raise ValidationError(_('You must specify either a country or a city.'))
        if self.country and self.city:
            raise ValidationError(_('Please indicate only the country OR only the city.'))

    def __str__(self):
        if self.city:
            return f"{self.packets.title} - {self.city.name}: ${self.price}"
        elif self.country:
            return f"{self.packets.title} - {self.country.name}: ${self.price}"
        return f"{self.packets.title}: ${self.price}"


class News(TranslationMixin):
    countries = models.ManyToManyField(Country, blank=True, verbose_name=_('Countries'),
                                       help_text=_('News will be shown in all selected countries'))
    cities = models.ManyToManyField(City, blank=True, verbose_name=_('Cities'),
                                    help_text=_(
                                        'News will be shown only in these cities (even if country is selected)'))

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=255, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=255, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=255, blank=True, verbose_name="Title (UK)")

    description = models.TextField(default='Description will be here soon', verbose_name=_('Description'))
    description_en = models.TextField(blank=True, default='', verbose_name="Description (EN)")
    description_de = models.TextField(blank=True, default='', verbose_name="Description (DE)")
    description_nl = models.TextField(blank=True, default='', verbose_name="Description (NL)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Description (RU)")
    description_uk = models.TextField(blank=True, default='', verbose_name="Description (UK)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    photo = models.ImageField(upload_to='news_photos/', blank=True, null=True)
    watched = models.IntegerField(default=0, verbose_name=_('Views'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='news', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.get_translated_field('title')

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ['-created_at']


class Stocks(TranslationMixin):
    countries = models.ManyToManyField(Country, blank=True, verbose_name=_('Countries'),
                                       help_text=_('Stock will be shown in all selected countries'))
    cities = models.ManyToManyField(City, blank=True, verbose_name=_('Cities'),
                                    help_text=_(
                                        'Stock will be shown only in these cities (even if country is selected)'))

    title = models.CharField(max_length=255, verbose_name=_('Title'))
    title_en = models.CharField(max_length=255, blank=True, verbose_name="Title (EN)")
    title_de = models.CharField(max_length=255, blank=True, verbose_name="Title (DE)")
    title_nl = models.CharField(max_length=255, blank=True, verbose_name="Title (NL)")
    title_ru = models.CharField(max_length=255, blank=True, verbose_name="Title (RU)")
    title_uk = models.CharField(max_length=255, blank=True, verbose_name="Title (UK)")

    description = models.TextField(default='Description will be here soon', verbose_name=_('Description'))
    description_en = models.TextField(blank=True, default='', verbose_name="Description (EN)")
    description_de = models.TextField(blank=True, default='', verbose_name="Description (DE)")
    description_nl = models.TextField(blank=True, default='', verbose_name="Description (NL)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Description (RU)")
    description_uk = models.TextField(blank=True, default='', verbose_name="Description (UK)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    photo = models.ImageField(upload_to='stocks_photos/', blank=True, null=True)
    watched = models.IntegerField(default=0, verbose_name=_('Views'))
    is_published = models.BooleanField(default=True, verbose_name=_('Published'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'),
                                 related_name='stocks', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)

    def get_absolute_url(self):
        return reverse('stocks_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.get_translated_field('title')

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')
        ordering = ['-created_at']

class Profile(models.Model):
    """Расширение стандартной модели User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, verbose_name=_('Phone number'), blank=True)
    address = models.TextField(verbose_name=_('Address'), blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('City'))
    # Для платежей и подписок
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Balance'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Verified'))
    preferred_contact_methods = models.JSONField(
        default=list,
        verbose_name=_('Preferred contact methods')
    )

    def save(self, *args, **kwargs):
        # Если поле пустое, устанавливаем все методы для связи с пользователем по умолчанию
        if not self.preferred_contact_methods:
            self.preferred_contact_methods = ['email', 'whatsapp', 'telegram', 'phone_call']
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Payment(models.Model):
    """Платеж пользователя"""
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SUCCEEDED = 'succeeded', _('Succeeded')
        FAILED = 'failed', _('Failed')
        REFUNDED = 'refunded', _('Refunded')

    class PaymentMethod(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        YOOKASSA = 'yookassa', 'ЮKassa'
        ROBOKASSA = 'robokassa', 'Robokassa'
        PAYPAL = 'paypal', 'PayPal'
        MOCK = 'mock', 'Mock (development)'

    class TransactionType(models.TextChoices):
        DEPOSIT = 'deposit', _('Deposit')
        PAYMENT = 'payment', _('Payment')
        REFUND = 'refund', _('Refund')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    currency = models.CharField(max_length=3, default='USD', verbose_name=_('Currency'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    transaction_id = models.CharField(max_length=255, unique=True, db_index=True, verbose_name=_('Transaction ID'))
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.PAYMENT)
    payment_data = models.JSONField(default=dict, verbose_name=_('Payment data'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency}"

class CurrencyRate(models.Model):
    currency = models.CharField(max_length=3, unique=True, verbose_name='Currency Code')  # USD, EUR, RUB
    rate_to_usd = models.DecimalField(max_digits=10, decimal_places=4,
                                      verbose_name='Rate to USD')  # сколько единиц валюты за 1 USD
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Currency Rate'
        verbose_name_plural = 'Currency Rates'

    def __str__(self):
        return f"{self.currency}:{self.rate_to_usd} USD"

# Реализовать
class ConnectionRequest(models.Model):
    """Заявка на подключение услугу/тариф/вакансию"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('converted', 'Converted to Subscription'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Тип объекта(только ОДНО поле должно быть заполнено)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, blank=True)
    separately = models.ForeignKey(Separately, on_delete=models.SET_NULL, null=True, blank=True)
    packet = models.ForeignKey(Packets, on_delete=models.SET_NULL, null=True, blank=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_method = models.CharField(max_length=100, blank=True)

    address = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Дла админа
    processed = models.BooleanField(default=False, verbose_name='Processed')
    notes = models.TextField(blank=True, verbose_name="Manager's Notes")

    # Ссылка на созданную подписку (опционально)
    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Related Subscription',
        help_text='Auto-filled when converted to subscription'
    )

    class Meta:
        verbose_name = _('Connection Request')
        verbose_name_plural = _('Connection Requests')
        ordering = ['-created_at']

    def __str__(self):
        item = self.get_item()
        return f"#{self.id} - {self.user.username if self.user else 'Anonymous'} -> {item.title if item else 'Unknown'}"

    def get_item(self):
        """Возвращает объект заявки"""
        if self.tariff: return self.tariff
        if self.separately: return self.separately
        if self.packet: return self.packet
        if self.vacancy: return self.vacancy
        return None

    def get_item_type(self):
        """Возвращает тип объекта"""
        if self.tariff: return 'tariff'
        if self.separately: return 'separately'
        if self.packet: return 'packet'
        if self.vacancy: return 'vacancy'
        return None

    def save(self, *args, **kwargs):
        # Автозаполнение контактов из профиля
        if self.user and not self.contact_email:
            self.contact_email = self.user.email
            profile = getattr(self.user, 'profile', None)
            if profile:
                self.contact_phone = profile.phone or ''
                if profile.preferred_contact_methods:
                    self.contact_method = profile.preferred_contact_methods[0]
                self.address = profile.address or ''
                self.city = profile.city

        super().save(*args, **kwargs)

class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_numbers')
    number = PhoneNumberField(verbose_name=_('Phone number'))
    verified = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True)
    code_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'number')
        verbose_name = _('Phone number')
        verbose_name_plural = _('Phone numbers')

    def generate_code(self):
        self.verification_code = f"{random.randint(100000, 999999)}"
        self.code_sent_at = timezone.now()
        self.save()

    def __str__(self):
        return str(self.number)

class Subscription(models.Model):
    """Подписка пользователя на тариф"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, verbose_name=_('Tariff'))
    start_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Start date'))
    end_date = models.DateTimeField(verbose_name=_('End date'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    auto_renew = models.BooleanField(default=True, verbose_name=_('Auto renew'))

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f"{self.user.username} - {self.tariff.title if self.tariff else 'No tariff'}"

class FAQ(TranslationMixin):
    question = models.CharField(max_length=255, verbose_name=_('Question'))
    question_en = models.CharField(max_length=255, blank=True, verbose_name="Question (EN)")
    question_de = models.CharField(max_length=255, blank=True, verbose_name="Question (DE)")
    question_nl = models.CharField(max_length=255, blank=True, verbose_name="Question (NL)")
    # ADDED FOR UKRAINIAN AND RUSSIAN
    question_ru = models.CharField(max_length=255, blank=True, verbose_name="Question (RU)")
    question_uk = models.CharField(max_length=255, blank=True, verbose_name="Question (UK)")

    answer = models.TextField(verbose_name=_('Answer'))
    answer_en = models.TextField(blank=True, default='', verbose_name="Answer (EN)")
    answer_de = models.TextField(blank=True, default='', verbose_name="Answer (DE)")
    answer_nl = models.TextField(blank=True, default='', verbose_name="Answer (NL)")
    # ADDED FOR UKRAINIAN AND RUSSIAN
    answer_ru = models.TextField(blank=True, default='', verbose_name="Answer (RU)")
    answer_uk = models.TextField(blank=True, default='', verbose_name="Answer (UK)")

    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        ordering = ['order']
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

    def __str__(self):
        return self.get_translated_field('question')


class SupportTicket(TranslationMixin):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('in_progress', _('In progress')),
        ('resolved', _('Resolved')),
        ('closed', _('Closed')),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('User'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    email = models.EmailField(verbose_name=_('Email'))

    subject = models.CharField(max_length=200, verbose_name=_('Subject'))
    subject_en = models.CharField(max_length=200, blank=True, verbose_name="Subject (EN)")
    subject_de = models.CharField(max_length=200, blank=True, verbose_name="Subject (DE)")
    subject_nl = models.CharField(max_length=200, blank=True, verbose_name="Subject (NL)")
    subject_ru = models.CharField(max_length=200, blank=True, verbose_name="Subject (RU)")
    subject_uk = models.CharField(max_length=200, blank=True, verbose_name="Subject (UK)")

    message = models.TextField(verbose_name=_('Message'))
    message_en = models.TextField(blank=True, default='', verbose_name="Message (EN)")
    message_de = models.TextField(blank=True, default='', verbose_name="Message (DE)")
    message_nl = models.TextField(blank=True, default='', verbose_name="Message (NL)")
    message_ru = models.TextField(blank=True, default='', verbose_name="Message (RU)")
    message_uk = models.TextField(blank=True, default='', verbose_name="Message (UK)")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Support ticket')
        verbose_name_plural = _('Support tickets')

    def __str__(self):
        return f"#{self.id} - {self.get_translated_field('subject')}"