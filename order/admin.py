from django.contrib import admin

from .models import OrderItem, Order

admin.site.register(Order)


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'product', 'quantity')
