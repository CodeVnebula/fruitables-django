from django.db import models
from django.db.models import Count, Prefetch

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def get_categories_with_children(self, category_slug=None):
        if category_slug:
            print('______________________Category slug____________________________________')
            return self.get_queryset().filter(slug=category_slug).prefetch_related('children').prefetch_related(Prefetch(
                'children__products'
            )).annotate(
                products_count=Count('children__products')
            ).filter(products_count__gt=0)
        
        print('_______________________NO___________________________________')
        return self.get_queryset().prefetch_related('children').prefetch_related(Prefetch(
            'children__products'
        )).annotate(
            products_count=Count('children__products')
        ).filter(products_count__gt=0)
    
    def get_root_categories(self):
        return self.get_queryset().filter(parent=None)
    
    
    
class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)
    
    def get_products_by_category_slug(self, category_slug):
        return self.get_queryset().filter(category__slug=category_slug, is_available=True)