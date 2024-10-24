from django.shortcuts import render
from .models import Testimonial
from store.views import cart_view

def about(request):
    # return render(request, 'about.html')
    pass

def contact(request):
    items_in_cart = cart_view(request)[0]
    context = {
        'items_in_cart': items_in_cart
    }
    return render(request, 'contact.html', context)

def testimonial(request):
    items_in_cart = cart_view(request)[0]
    context = {
        'items_in_cart': items_in_cart
    }
    
    testimonies = Testimonial.objects.all()
    
    testimonials = []
    for testimony in testimonies:
        filled_stars = '<i class="fa fa-star text-secondary"></i>' * testimony.stars
        empty_stars = '<i class="fa fa-star"></i>' * (5 - testimony.stars)
        star_html = filled_stars + empty_stars
        
        testimonials.append({
            'client_name':testimony.client_name,
            'testimonial_text':testimony.testimonial_text,
            'stars':star_html,
            'image':testimony.client_image.url if testimony.client_image else None
        })
    
    context = {
        'items_in_cart': items_in_cart,
        'testimonials':testimonials[:10]
    }
    return render(request, 'testimonial.html', context)

