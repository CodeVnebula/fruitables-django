from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.header_search, name='header_search'),
    path('product/<slug:product_slug>/', views.product_details, name='product_details'),
    path('category/<slug:category_slug>/', views.category_products, name='category_products'),
    path('add-to-cart/<int:product_id>/<str:weight>/', views.add_to_cart, name='add_to_cart_weight'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
