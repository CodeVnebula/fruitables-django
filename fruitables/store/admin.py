from django.contrib import admin
from .models import Category, Product, Review, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['parent'] 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'pack_weight', 'country_of_origin', 'quality', 'health_check']
    search_fields = ['name', 'country_of_origin', 'quality', 'health_check', 'category__name']
    list_filter = ['category', 'stars', 'is_available']
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'reviewer_name', 'reviewer_email', 'created_at']
    search_fields = ['product__name', 'reviewer_name', 'reviewer_email']
    list_filter = ['product']
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
