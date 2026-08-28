from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Page routes
    path('', views.home_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('cctv/', views.cctv_view, name='cctv'),
    path('networking/', views.networking_view, name='networking'),
    path('repairs/', views.repairs_view, name='repairs'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail_view, name='portfolio_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('shop/', views.shop_view, name='shop'),

    # API endpoints
    path('api/repair-estimate/', views.estimate_repair_cost_api, name='api_repair_estimate'),
    path('api/booking/create/', views.create_booking_api, name='api_create_booking'),
    path('api/repair/track/', views.track_repair_api, name='api_track_repair'),
    path('api/contact/', views.contact_submit_api, name='api_contact_submit'),
    path('api/shop/order/', views.create_shop_order_api, name='api_shop_order'),
    path('api/shop/verify-payment/', views.verify_paystack_payment_api, name='api_verify_payment'),
]
