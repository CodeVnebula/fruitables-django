from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop_view'),
    path('shop/category/<slug:category_slug>/', views.shop_view, name='shop_view'),
    path('product/<slug:product_slug>/', views.product_view, name='product_view'),
]
