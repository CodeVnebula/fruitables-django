from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import ContactForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

def home_view(request):
    return render(request, 'index.html')

def about_view(request):
    pass

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages
from .forms import ContactForm  
from decouple import AutoConfig
from textwrap import dedent
from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings

def set_language_custom(request):
    language = request.POST.get('language', settings.LANGUAGE_CODE)
    activate(language)
    response = redirect(request.POST.get('next', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "contact.html"
    login_url = '/user/login/'
    redirect_field_name = 'next'
    config = AutoConfig()
    ADMIN_EMAIL = config('ADMIN_EMAIL')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You need to be signed in to send a message.")
        return super().dispatch(request, *args, **kwargs) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm() 
        return context

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            
            msg = dedent(f"""
                        You have received a new message from your contact form:

                        Name: {name}
                        Subject: {subject}
                        Email: {from_email}
                        Message: {message}

                        Please reply to {from_email} if you need to contact them.
                    """)
            
            try:
                send_mail(
                    subject=subject,
                    message=msg,
                    from_email=from_email,
                    recipient_list=[self.ADMIN_EMAIL],
                )
                messages.success(request, "Email sent successfully. Thank you for contacting us. We will get back to you soon.")
                return redirect('contact')  
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {'form': form})


def testimonial_view(request):
    # return render(request, 'pages/testimonial.html')
    pass

class Custom404View(TemplateView):
    template_name = "404.html"
    def custom_404_view(self, request, exception):
        return render(request, self.template_name, status=404)
class Custom500View(TemplateView):
    template_name = "500.html"
    def custom_404_view(self, request, exception):
        return render(request, self.template_name, status=500)
    