from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('testimonial/', views.testimonial_view, name='testimonial_view'),
]

handler404 = views.Custom404View
handler500 = views.Custom500View
