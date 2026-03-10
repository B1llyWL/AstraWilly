from django.urls import path, include
from django.views.i18n import set_language, JavaScriptCatalog
from .views import  main, news, profile, api, phone, payment, support

from .views.profile import UsernameChangeView

urlpatterns = [
    path('', main.HomePageView.as_view(), name='home'),
    path('tariffs/', main.tariffs, name='tariffs'),
    path('services/', main.services, name='services'),
    path('vacancy/', main.vacancy_view, name='vacancy'),
    path('set-location/', main.set_location, name='set_location'),
    path('get-cities/', main.get_cities, name='get_cities'),
    path('news/', news.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', news.NewsDetailView.as_view(), name='news_detail'),
    path('search/', main.search, name='search'),
    path('stocks/', news.StocksListView.as_view(), name='stocks'),
    path('stocks/<slug:slug>/', news.StocksDetailView.as_view(), name='stocks_detail'),
    path('api/find-location/', main.find_location, name='find_location'),
    path('i18n/', set_language, name='set_language'),
    path('jsi18n/', JavaScriptCatalog.as_view(),name='javascript-catalog'),
    path('profile/', profile.profile_view, name='profile'),
    path('profile/edit/', profile.edit_profile, name='edit_profile'),
    path('profile/username/', UsernameChangeView.as_view(), name='change_username'),
    path('accounts/', include('allauth.urls')),
    path('accounts/username/change/', profile.UsernameChangeView.as_view(), name='account_change_username'),
    path('quick-connect/<str:item_type>/<int:item_id>/', api.quick_connect, name='quick_connect'),
    path('cancel-request/<int:request_id>/', api.cancel_connection_request, name='cancel_request'),
    path('change-tariff/<int:tariff_id>/', api.change_tariff, name='change_tariff'),
    path('purchase-separately/<int:separately_id>/', api.purchase_separately, name='purchase_separately'),
    path('purchase-packets/<int:packets_id>/',api.purchase_packets, name='purchase_packets'),
    path('phone/', phone.phone_list, name='phone_list'),
    path('phone/add/', phone.phone_add, name='phone_add'),
    path('phone/verify/<int:phone_id>', phone.phone_verify, name='phone_verify'),
    path('phone/make-primary/<int:phone_id>/', phone.phone_make_primary, name='phone_make_primary'),
    path('phone/remove/<int:phone_id>/', phone.phone_remove, name='phone_remove'),
    path('phone/resend/<int:phone_id>/', phone.phone_resend, name='phone_resend'),
    path('request/<str:item_type>/<int:item_id>/', api.create_connection_request, name='create_request'),
    path('request/<int:request_id>/cancel/', api.cancel_connection_request, name='cancel_request'),
    path('payment/create/', payment.create_payment, name='create_payment'),
    path('support/', support.support, name='support'),
]