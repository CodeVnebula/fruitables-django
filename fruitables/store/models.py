import os
from django.db import models
from django.utils.text import slugify
from .managers import CategoryManager, ProductManager
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Category name'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children', verbose_name=_('Parent category'))
    slug = models.SlugField(max_length=255, unique=False, blank=True, default='', verbose_name=_('Slug'))  
    
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
    name = models.CharField(max_length=255, verbose_name=_('Product name'))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Price'))
    description = models.TextField(verbose_name=_('Description'))
    detailed_description = models.TextField(null=True, blank=True, default='', verbose_name=_('Detailed description'))
    pack_weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Pack weight'))
    min_weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Min weight'))
    country_of_origin = models.CharField(max_length=255, verbose_name=_('Country of origin'))
    quality = models.CharField(max_length=255, verbose_name=_('Quality'))
    health_check = models.CharField(max_length=255, verbose_name=_('Health check'))
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name=_('Image'))
    stars = models.IntegerField(default=0, verbose_name=_('Stars'))
    reviews_amount = models.IntegerField(default=0, verbose_name=_('Reviews amount'))
    category = models.ManyToManyField(Category, related_name='products', verbose_name=_('Category'))
    tag = models.ManyToManyField('Tag', related_name='products', blank=True, verbose_name=_('Tag'))
    review = models.ManyToManyField('Review', related_name='products', blank=True, verbose_name=_('Review'))
    slug = models.SlugField(max_length=255, unique=True, blank=True, default='', verbose_name=_('Slug'))
    weight_available = models.FloatField(default=0, verbose_name=_('Weight available'))
    is_available = models.BooleanField(default=True, editable=True, blank=True, verbose_name=_('Is available'))
    
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
        
        if self.image:
            from PIL import Image
            from io import BytesIO
            from django.core.files.base import ContentFile
            img = Image.open(self.image)
            width, height = img.size

            max_height = 235
            if height > max_height:
                new_height = max_height
                new_width = int((max_height / height) * width)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=90)
                self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)

        
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Product'))
    reviewer_name = models.CharField(max_length=100, verbose_name=_('Reviewer name'))
    reviewer_email = models.EmailField(verbose_name=_('Reviewer email'))
    review = models.TextField(verbose_name=_('Review'))
    stars = models.IntegerField(default=0, verbose_name=_('Stars'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    
    def __str__(self):
        return self.reviewer_name


class Tag(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
