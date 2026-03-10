from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import (
    Tariff, Category, Vacancy, Place, Language, Country, News,
    TariffPrice, City, SeparatelyPrice, Separately, Packets,
    PacketsPrice, VacancyLocation, Stocks, CurrencyRate,
    SupportTicket, FAQ, Profile, Subscription, Payment, ConnectionRequest
)

class VacancyLocationInline(admin.TabularInline):
    model = VacancyLocation
    extra = 1
    filter_horizontal = ('languages',)
    autocomplete_fields = ('place',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'currency')
    search_fields = ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk', 'code')
    list_filter = ('currency',)
    list_per_page = 20

    fieldsets = (
        (_('Name'), {
            'fields': ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk')
        }),
        (_('Additional'), {
            'fields': ('code', 'currency')
        }),
    )

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_country')
    list_filter = ('country',)
    search_fields = ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk', 'country__name')
    list_per_page = 20

    fieldsets = (
        (_('Name'), {
            'fields': ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk')
        }),
        (_('Location'), {
            'fields': ('country',)
        }),
    )

    def display_country(self, obj):
        return obj.country.name
    display_country.short_description = _('Country')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk')
    list_per_page = 20

    fieldsets = (
        (_('Title'), {
            'fields': ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk')
        }),
        (_('Additional'), {
            'fields': ('slug', 'parent')
        }),
    )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk')
    list_per_page = 20

    fieldsets = (
        (_('Name'), {
            'fields': ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk')
        }),
    )

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'address')
    list_filter = ('country', 'city')
    search_fields = ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk',
                     'address', 'address_en', 'address_de', 'address_nl', 'address_ru', 'address_uk',
                     'city__name')
    autocomplete_fields = ['country', 'city']
    list_per_page = 20

    fieldsets = (
        (_('Name'), {
            'fields': ('name', 'name_en', 'name_de', 'name_nl', 'name_ru', 'name_uk')
        }),
        (_('Address'), {
            'fields': ('address', 'address_en', 'address_de', 'address_nl', 'address_ru', 'address_uk')
        }),
        (_('Location'), {
            'fields': ('country', 'city')
        }),
    )

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'order', 'created_at', 'watched')
    list_editable = ('price', 'category', 'order')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'price', 'created_at')
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                     'description', 'description_en', 'description_de', 'description_nl',
                     'description_ru', 'description_uk')
    list_per_page = 20
    sortable_by = ['order']
    ordering = ['order', 'title']
    readonly_fields = ('watched', 'created_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                       'slug', 'price', 'category', 'order')
        }),
        (_('Description'), {
            'fields': ('description', 'description_en', 'description_de', 'description_nl',
                       'description_ru', 'description_uk')
        }),
        (_('Features'), {
            'fields': ('features_text', 'features_text_en', 'features_text_de', 'features_text_nl',
                       'features_text_ru', 'features_text_uk'),
            'description': _('Each feature on a new line.')
        }),
        (_('Statistics (read-only)'), {
            'fields': ('watched', 'created_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.order:
            max_order = Tariff.objects.aggregate(models.Max('order'))['order__max'] or 0
            obj.order = max_order + 1
        super().save_model(request, obj, form, change)

@admin.register(Separately)
class SeparatelyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'order', 'created_at', 'watched')
    list_editable = ('price', 'category', 'order')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'price', 'created_at')
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                     'description', 'description_en', 'description_de', 'description_nl',
                     'description_ru', 'description_uk')
    list_per_page = 20
    sortable_by = ['order']
    ordering = ['order', 'title']
    readonly_fields = ('watched', 'created_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                       'slug', 'price', 'category', 'order')
        }),
        (_('Description'), {
            'fields': ('description', 'description_en', 'description_de', 'description_nl',
                       'description_ru', 'description_uk')
        }),
        (_('Features'), {
            'fields': ('features_text', 'features_text_en', 'features_text_de', 'features_text_nl',
                       'features_text_ru', 'features_text_uk'),
            'description': _('Each feature on a new line.')
        }),
        (_('Statistics (read-only)'), {
            'fields': ('watched', 'created_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.order:
            max_order = Separately.objects.aggregate(models.Max('order'))['order__max'] or 0
            obj.order = max_order + 1
        super().save_model(request, obj, form, change)

@admin.register(Packets)
class PacketsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'order', 'created_at', 'watched')
    list_editable = ('price', 'category', 'order')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'price', 'created_at')
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                     'description', 'description_en', 'description_de', 'description_nl',
                     'description_ru', 'description_uk')
    list_per_page = 20
    sortable_by = ['order']
    ordering = ['order', 'title']
    readonly_fields = ('watched', 'created_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                       'slug', 'price', 'category', 'order')
        }),
        (_('Description'), {
            'fields': ('description', 'description_en', 'description_de', 'description_nl',
                       'description_ru', 'description_uk')
        }),
        (_('Features'), {
            'fields': ('features_text', 'features_text_en', 'features_text_de', 'features_text_nl',
                       'features_text_ru', 'features_text_uk'),
            'description': _('Each feature on a new line.')
        }),
        (_('Statistics (read-only)'), {
            'fields': ('watched', 'created_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.order:
            max_order = Packets.objects.aggregate(models.Max('order'))['order__max'] or 0
            obj.order = max_order + 1
        super().save_model(request, obj, form, change)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'has_html', 'price', 'created_at', 'locations_summary',
                    'display_countries', 'is_published', 'watched')
    list_editable = ('price', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('countries', 'is_published', 'category')
    list_display_links = ('title',)
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                     'description', 'description_en', 'description_de', 'description_nl',
                     'description_ru', 'description_uk')
    list_per_page = 20
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 10, 'cols': 80, 'style': 'width: 95%;'})},
    }

    inlines = [VacancyLocationInline]
    readonly_fields = ('watched', 'created_at', 'updated_at', 'preview_image', 'countries')

    fieldsets = (
        (_('Main information'), {
            'fields': ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                       'slug', 'price', 'category', 'is_published', 'photo', 'preview_image')
        }),
        (_('Description (simple)'), {
            'fields': ('description', 'description_en', 'description_de', 'description_nl',
                       'description_ru', 'description_uk',
                       'features_text', 'features_text_en', 'features_text_de', 'features_text_nl',
                       'features_text_ru', 'features_text_uk'),
            'description': _('Used if HTML description is empty. Each feature on a new line.')
        }),
        (_('Description (HTML)'), {
            'fields': ('details_html', 'details_html_en', 'details_html_de', 'details_html_nl',
                       'details_html_ru', 'details_html_uk'),
            'description': _('Full HTML description. Overrides simple description if filled.')
        }),
        (_('Statistics (read-only)'), {
            'fields': ('watched', 'created_at', 'updated_at', 'countries'),
            'classes': ('collapse',)
        })
    )

    def has_html(self, obj):
        return bool(obj.details_html)
    has_html.boolean = True
    has_html.short_description = _('Has HTML')

    def preview_image(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" style="max-height: 200px;" />')
        return _("No image")
    preview_image.short_description = _('Preview')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.watched = 0
        super().save_model(request, obj, form, change)

    def locations_summary(self, obj):
        count = obj.locations.count()
        if count == 0:
            return "—"
        first = obj.locations.first()
        place_str = first.place.address or first.place.name or _("No address")
        return f"{count} {_('office(s)')}: {place_str}"
    locations_summary.short_description = _('Offices')

    def display_countries(self, obj):
        countries = obj.countries.all()
        return ", ".join([c.name for c in countries]) if countries else "—"
    display_countries.short_description = _('Countries')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_countries_display', 'get_cities_display', 'category',
                    'created_at', 'updated_at', 'is_published', 'watched')
    filter_horizontal = ('countries', 'cities')
    actions = ['add_all_cities_from_countries']
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                     'description', 'description_en', 'description_de', 'description_nl',
                     'description_ru', 'description_uk')
    list_per_page = 20
    readonly_fields = ('watched', 'created_at', 'updated_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('countries', 'cities', 'title', 'title_en', 'title_de', 'title_nl',
                       'title_ru', 'title_uk', 'slug', 'category', 'is_published', 'photo')
        }),
        (_('Content'), {
            'fields': ('description', 'description_en', 'description_de', 'description_nl',
                       'description_ru', 'description_uk'),
            'classes': ('wide',)
        }),
        (_('Statistics (read-only)'), {
            'fields': ('watched', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_countries_display(self, obj):
        countries = obj.countries.all()
        return ", ".join([c.name for c in countries[:3]]) + ("..." if countries.count() > 3 else "")
    get_countries_display.short_description = _('Countries')

    def get_cities_display(self, obj):
        cities = obj.cities.all()
        return ", ".join([c.name for c in cities[:3]]) + ("..." if cities.count() > 3 else "")
    get_cities_display.short_description = _('Cities')

    def add_all_cities_from_countries(self, request, queryset):
        for news in queryset:
            cities_to_add = City.objects.filter(country__in=news.countries.all())
            news.cities.add(*cities_to_add)
        self.message_user(request, _("Cities added for selected news"))
    add_all_cities_from_countries.short_description = _("Add all cities from selected countries")

@admin.register(Stocks)
class StocksAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_countries_display', 'get_cities_display', 'category',
                    'created_at', 'updated_at', 'is_published', 'watched')
    filter_horizontal = ('countries', 'cities')
    actions = ['add_all_cities_from_countries']
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'is_published', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title', 'title_en', 'title_de', 'title_nl', 'title_ru', 'title_uk',
                     'description', 'description_en', 'description_de', 'description_nl',
                     'description_ru', 'description_uk')
    list_per_page = 20
    readonly_fields = ('watched', 'created_at', 'updated_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('countries', 'cities', 'title', 'title_en', 'title_de', 'title_nl',
                       'title_ru', 'title_uk', 'slug', 'category', 'is_published', 'photo')
        }),
        (_('Content'), {
            'fields': ('description', 'description_en', 'description_de', 'description_nl',
                       'description_ru', 'description_uk'),
            'classes': ('wide',)
        }),
        (_('Statistics (read-only)'), {
            'fields': ('watched', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_countries_display(self, obj):
        countries = obj.countries.all()
        return ", ".join([c.name for c in countries[:3]]) + ("..." if countries.count() > 3 else "")
    get_countries_display.short_description = _('Countries')

    def get_cities_display(self, obj):
        cities = obj.cities.all()
        return ", ".join([c.name for c in cities[:3]]) + ("..." if cities.count() > 3 else "")
    get_cities_display.short_description = _('Cities')

    def add_all_cities_from_countries(self, request, queryset):
        for stocks in queryset:
            cities_to_add = City.objects.filter(country__in=stocks.countries.all())
            stocks.cities.add(*cities_to_add)
        self.message_user(request, _("Cities added for selected stocks"))
    add_all_cities_from_countries.short_description = _("Add all cities from selected countries")

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'question_en', 'question_de', 'question_nl', 'question_ru', 'question_uk',
                     'answer', 'answer_en', 'answer_de', 'answer_nl', 'answer_ru', 'answer_uk')

    fieldsets = (
        (_('Question'), {
            'fields': ('question', 'question_en', 'question_de', 'question_nl', 'question_ru', 'question_uk')
        }),
        (_('Answer'), {
            'fields': ('answer', 'answer_en', 'answer_de', 'answer_nl', 'answer_ru', 'answer_uk')
        }),
        (_('Additional'), {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email',
                     'subject', 'subject_en', 'subject_de', 'subject_nl', 'subject_ru', 'subject_uk',
                     'message', 'message_en', 'message_de', 'message_nl', 'message_ru', 'message_uk')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('User'), {
            'fields': ('user', 'name', 'email')
        }),
        (_('Subject'), {
            'fields': ('subject', 'subject_en', 'subject_de', 'subject_nl', 'subject_ru', 'subject_uk')
        }),
        (_('Message'), {
            'fields': ('message', 'message_en', 'message_de', 'message_nl', 'message_ru', 'message_uk')
        }),
        (_('Status'), {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate_to_usd', 'updated_at')
    list_editable = ('rate_to_usd',)
    search_fields = ('currency',)
    list_per_page = 20

@admin.register(TariffPrice)
class TariffPriceAdmin(admin.ModelAdmin):
    list_display = ('tariff', 'display_country', 'display_city', 'price', 'display_category', 'created_at', 'updated_at')
    list_filter = ('country', 'city', 'tariff')
    list_editable = ('price',)
    search_fields = ('tariff__title', 'country__name', 'city__name')
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('tariff', 'price')
        }),
        (_('Location'), {
            'fields': ('country', 'city'),
            'description': _('Specify either a country or a city. Do not fill both.')
        }),
        (_('Dates (read-only)'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def display_country(self, obj):
        if obj.country:
            return obj.country.name
        elif obj.city:
            return obj.city.country.name
        return "—"
    display_country.short_description = _('Country')

    def display_city(self, obj):
        if obj.city:
            return obj.city.name
        return "—"
    display_city.short_description = _('City')

    def display_category(self, obj):
        return obj.tariff.category.title if obj.tariff.category else "—"
    display_category.short_description = _('Category')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "city":
            kwargs["queryset"] = City.objects.select_related('country').order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(SeparatelyPrice)
class SeparatelyPriceAdmin(admin.ModelAdmin):
    list_display = ('separately', 'display_country', 'display_city', 'price', 'display_category', 'created_at', 'updated_at')
    list_filter = ('country', 'city', 'separately')
    list_editable = ('price',)
    search_fields = ('separately__title', 'country__name', 'city__name')
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('separately', 'price')
        }),
        (_('Location'), {
            'fields': ('country', 'city'),
            'description': _('Specify either a country or a city. Do not fill both.')
        }),
        (_('Dates (read-only)'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def display_country(self, obj):
        if obj.country:
            return obj.country.name
        elif obj.city:
            return obj.city.country.name
        return "—"
    display_country.short_description = _('Country')

    def display_city(self, obj):
        if obj.city:
            return obj.city.name
        return "—"
    display_city.short_description = _('City')

    def display_category(self, obj):
        return obj.separately.category.title if obj.separately.category else "—"
    display_category.short_description = _('Category')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "city":
            kwargs["queryset"] = City.objects.select_related('country').order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(PacketsPrice)
class PacketsPriceAdmin(admin.ModelAdmin):
    list_display = ('packets', 'display_country', 'display_city', 'price', 'display_category', 'created_at', 'updated_at')
    list_filter = ('country', 'city', 'packets')
    list_editable = ('price',)
    search_fields = ('packets__title', 'country__name', 'city__name')
    list_per_page = 20
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (_('Main information'), {
            'fields': ('packets', 'price')
        }),
        (_('Location'), {
            'fields': ('country', 'city'),
            'description': _('Specify either a country or a city. Do not fill both.')
        }),
        (_('Dates (read-only)'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def display_country(self, obj):
        if obj.country:
            return obj.country.name
        elif obj.city:
            return obj.city.country.name
        return "—"
    display_country.short_description = _('Country')

    def display_city(self, obj):
        if obj.city:
            return obj.city.name
        return "—"
    display_city.short_description = _('City')

    def display_category(self, obj):
        return obj.packets.category.title if obj.packets.category else "—"
    display_category.short_description = _('Category')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "city":
            kwargs["queryset"] = City.objects.select_related('country').order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'balance', 'is_verified')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('is_verified', 'city')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'currency', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'transaction_id')

@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'get_item_type', 'item_info', 'contact_email_display',
                    'contact_phone_display', 'contact_method', 'short_address', 'status',
                    'created_at', 'processed', 'has_subscription')
    list_filter = ('status', 'processed', 'created_at')
    search_fields = ('user__username', 'contact_email', 'contact_phone', 'address')
    list_editable = ('status', 'processed',)
    readonly_fields = ('created_at', 'updated_at', 'full_contact_info', 'subscription')

    actions = ['approve_requests', 'reject_requests']

    fieldsets = (
        (_('Request'), {
            'fields': ('user', 'status', 'processed', 'subscription')
        }),
        (_('Item'), {
            'fields': ('tariff', 'separately', 'packet', 'vacancy')
        }),
        (_('Contact Information'), {
            'fields': ('contact_email', 'contact_phone', 'contact_method', 'address', 'city')
        }),
        (_('Full Contact Info'), {
            'fields': ('full_contact_info',),
            'classes': ('collapse',)
        }),
        (_('Dates'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        (_('Manager Notes'), {
            'fields': ('notes',)
        }),
    )

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.pk])
            return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
        return "Anonymous"
    user_link.short_description = _('User')

    def item_info(self, obj):
        item = obj.get_item()
        item_type = obj.get_item_type()
        if item:
            return f"{item_type.capitalize()}: {item.title}"
        return "-"
    item_info.short_description = _('Item')

    def contact_info(self, obj):
        parts = []
        if obj.contact_email:
            parts.append(f"✉️ {obj.contact_email}")
        if obj.contact_phone:
            parts.append(f"📱 {obj.contact_phone}")
        return mark_safe('<br>'.join(parts)) if parts else "—"
    contact_info.short_description = _('Contact')

    def has_subscription(self, obj):
        if obj.subscription:
            return mark_safe('<span style="color: green;">✅ Yes</span>')
        return mark_safe('<span style="color: grey;">-</span>')
    has_subscription.short_description = _('Subscription')

    def full_contact_info(self, obj):
        if not obj.user:
            return _("Anonymous user")

        html = f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #8338ec;">
            <h4 style="margin-top: 0;">{obj.user.username}</h4>
            <p><strong>📧 Email:</strong> <a href="mailto:{obj.contact_email}">{obj.contact_email or '—'}</a></p>
            <p><strong>📱 Phone:</strong> {obj.contact_phone or '—'}</p>
            <p><strong>⭐ Preferred:</strong> {obj.contact_method or '—'}</p>
            <p><strong>📍 Address:</strong> {obj.address or '—'}</p>
            <p><strong>🏙️ City:</strong> {obj.city or '—'}</p>
            <p><strong>💰 Balance:</strong> ${getattr(obj.user.profile, 'balance', 0)}</p>
        </div>
        """
        return mark_safe(html)
    full_contact_info.short_description = _('Full Contact Information')

    def approve_requests(self, request, queryset):
        count = 0
        for req in queryset.filter(status='pending'):
            req.status = 'approved'
            req.save()
            count += 1
        self.message_user(request, f'{count} request(s) approved.')
    approve_requests.short_description = _('Approve selected requests')

    def reject_requests(self, request, queryset):
        count = 0
        for req in queryset.filter(status='pending'):
            req.status = 'rejected'
            req.save()
            count += 1
        self.message_user(request, f'{count} request(s) rejected.')
    reject_requests.short_description = _('Reject selected requests')

    def get_item_type(self, obj):
        return obj.get_item_type() or '-'
    get_item_type.short_description = _('Type')
    get_item_type.admin_order_field = 'tariff'

    def contact_email_display(self, obj):
        return obj.contact_email or '-'
    contact_email_display.short_description = _('Email')

    def contact_phone_display(self, obj):
        return obj.contact_phone or '-'
    contact_phone_display.short_description = _('Phone')

    def short_address(self, obj):
        if obj.address:
            return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
        return '-'
    short_address.short_description = _('Address')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tariff', 'start_date', 'end_date', 'is_active', 'auto_renew')
    list_filter = ('is_active', 'auto_renew', 'tariff')
    search_fields = ('user__username', 'tariff__title')
    list_editable = ('is_active',)

    fieldsets = (
        (_('Subscription'), {
            'fields': ('user', 'tariff', 'is_active', 'auto_renew')
        }),
        (_('Dates'), {
            'fields': ('start_date', 'end_date')
        }),
    )