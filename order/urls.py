from django.urls import path
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    order_summary,
    increase_quantity_item,
    checkout,
)

app_name = 'order'

urlpatterns = [
    path('order-summary', order_summary, name='order_summary'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', reduce_quantity_item, name='reduce-quantity-item'),
    path('increase-quantity-item/<pk>/', increase_quantity_item, name='increase-quantity-item'),
    path('checkout/', checkout, name='checkout')
]
