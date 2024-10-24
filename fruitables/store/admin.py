from django.contrib import admin
from .models import Category, Product, Review, Tag


from django.contrib import admin
from .models import Category

class NoParentFilter(admin.SimpleListFilter):
    title = 'No Parent'
    parameter_name = 'no_parent'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'No Parent'),
            ('no', 'Has Parent'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(parent__isnull=True)
        if self.value() == 'no':
            return queryset.filter(parent__isnull=False)
        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['parent', NoParentFilter] 


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
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
