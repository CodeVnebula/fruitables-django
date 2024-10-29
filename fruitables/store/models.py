import os
from django.db import models
from django.utils.text import slugify
from .managers import CategoryManager, ProductManager


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    slug = models.SlugField(max_length=255, unique=False, blank=True, default='')  
    
    objects = CategoryManager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        super(Category, self).save(*args, **kwargs)
        
    def get_all_children(self):
        children = self.children.all()
        for child in children:
            children = children | child.get_all_children()  
        return children
    
    def __str__(self):
        return self.name
    
    
  

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    detailed_description = models.TextField(null=True, blank=True, default='')
    pack_weight = models.DecimalField(max_digits=5, decimal_places=2)
    min_weight = models.DecimalField(max_digits=5, decimal_places=2)
    country_of_origin = models.CharField(max_length=255)
    quality = models.CharField(max_length=255)
    health_check = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stars = models.IntegerField(default=0)
    stars_count = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, related_name='products')
    tag = models.ManyToManyField('Tag', related_name='products', blank=True)
    review = models.ManyToManyField('Review', related_name='products', blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, default='')  
    weight_available = models.FloatField(default=0)
    is_available = models.BooleanField(default=True, editable=True, blank=True)
    
    objects = ProductManager()
    
    def _is_available(self):
        if self.weight_available <= self.min_weight * 10:
            return False
        return True

    def _get_min_weight_available(self):
        return self.min_weight * 10
    
    def delete(self, *args, **kwargs):
        if self.image and os.path.exists(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    reviewer_email = models.EmailField()
    review = models.TextField()
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.reviewer_name


class Tag(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
