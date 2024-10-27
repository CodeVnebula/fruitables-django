from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop_view'),
    path('shop/category/<slug:category_slug>/', views.ShopView.as_view(), name='show_view'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_view'),
]
