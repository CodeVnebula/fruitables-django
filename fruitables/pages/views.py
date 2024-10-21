from django.shortcuts import render

def about(request):
    # return render(request, 'about.html')
    pass

def contact(request):
    return render(request, 'contact.html')

def testimonial(request):
    return render(request, 'testimonial.html')

