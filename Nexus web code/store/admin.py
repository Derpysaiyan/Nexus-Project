

# Register your models here.
from django.contrib import admin
from .models import Product, SKU, Price, Inventory, Order, OrderItem, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "name")
    search_fields = ("brand", "name")

admin.site.register(SKU)
admin.site.register(Price)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CartItem)
