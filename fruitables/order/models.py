from django.db import models
from store.models import Product
from user.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_items_in_cart(self):
        return sum([1 for _ in self.items.all()])
    
    def __str__(self):
        return f"Cart {self.id} for User {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pack_weight = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_total_price(self):
        return round(self.product.price * self.pack_weight, 2)
    
    def __str__(self):
        return self.product.name


class CheckoutDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    order_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.user.username if self.user else "Guest"}'

