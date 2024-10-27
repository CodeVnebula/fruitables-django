from django.shortcuts import render

def home_view(request):
    return render(request, 'index.html')

def about_view(request):
    pass

def contact_view(request):
    return render(request, 'contact.html')

def testimonial_view(request):
    # return render(request, 'pages/testimonial.html')
    pass