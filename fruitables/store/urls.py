from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:product_slug>/', views.product_details, name='product_details'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
]
