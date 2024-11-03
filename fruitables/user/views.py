from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import User
from .forms import LoginForm, RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    next_page = reverse_lazy('account')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())  
    
    def get_success_url(self):
        user_slug = getattr(self.request.user, 'slug', None)
        return reverse_lazy('account', kwargs={'slug': user_slug or self.request.user.id})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    next_page = reverse_lazy('account')
    redirect_authenticated_user = True
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        user_slug = getattr(self.request.user, 'slug', None)
        return reverse_lazy('account', kwargs={'slug': user_slug or self.request.user.id})


class AccountView(LoginRequiredMixin, LoginView):
    template_name = 'account.html'
    login_url = 'login'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.user)
        return redirect('account')

    def get(self, request, slug=None, *args, **kwargs):
        user = get_object_or_404(User, slug=slug)
        
        if user != request.user:
            return redirect('account', slug=request.user.slug)

        context = {
            'user': user
        }
        return render(request, self.template_name, context)

