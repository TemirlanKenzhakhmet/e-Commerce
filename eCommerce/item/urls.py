from django.urls import path

from .views import (
    detail,
    create,
    delete,
    edit,
    search_list,
    search_results,
    add_to_cart,
    remove_from_cart,
    remove_item_from_cart,
    add_item_to_cart,
    OrderSummaryView,
    CheckoutView,
    PaymentView,
)

app_name = 'item'

urlpatterns = [
    path('', search_list, name='search'),
    path('htmx/search/', search_results, name='search-results'),
    path('create/', create, name='create'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('<slug:slug>', detail, name='detail'),
    path('<slug:slug>/delete/', delete, name='delete'),
    path('<slug:slug>/edit/', edit, name='edit'),
    path('add-to-cart/<slug:slug>', add_to_cart, name='add-to-cart'),
    path('add-item-to-cart/<slug:slug>', add_item_to_cart, name='add-item-to-cart'),
    path('remove-from-cart/<slug:slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug:slug>', remove_item_from_cart, name='remove-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]