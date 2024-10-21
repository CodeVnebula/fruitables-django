from django.contrib import admin
from .models import Category, Product, Review, Feature


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'pack_weight', 'country_of_origin', 'quality', 'health_check']
    search_fields = ['name', 'country_of_origin', 'quality', 'health_check', 'category__name']
    list_filter = ['category', 'stars']
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'reviewer_name', 'reviewer_email', 'created_at']
    search_fields = ['product__name', 'reviewer_name', 'reviewer_email']
    list_filter = ['product']
    

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'start_date', 'end_date']
    search_fields = ['title']
    list_filter = ['is_active']
