from django.contrib import admin
from . import models

@admin.register(models.CheckoutDetails)
class CheckoutDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user', 'created_at')
    ordering = ('created_at',)

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user', 'created_at')
    ordering = ('created_at',)
    
@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'pack_weight')
    search_fields = ('product', 'pack_weight')
