from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('apply-weight/<int:product_id>/', views.apply_weight, name='apply_weight'),
    path('delete-item/<int:product_id>/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
]
