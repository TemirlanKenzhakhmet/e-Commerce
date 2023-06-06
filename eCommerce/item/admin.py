from django.contrib import admin

from .models import Category, Item, Order, OrderItem, BillingAddress

class adminOrderItem(admin.ModelAdmin):
    list_display = ['id', 'item']

class adminItem(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']

admin.site.register(Category)
admin.site.register(Item, adminItem)
admin.site.register(Order)
admin.site.register(OrderItem, adminOrderItem)
admin.site.register(BillingAddress)