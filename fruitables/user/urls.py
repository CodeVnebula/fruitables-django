from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('account/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/<slug:slug>/', views.AccountView.as_view(), name='account'),
]


