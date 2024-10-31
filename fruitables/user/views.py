from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import User
from .forms import RegisterForm
from order.models import Cart
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(LoginView):
    template_name = 'register.html'
    next_page = 'account'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Cart.objects.create(user=user)
            return redirect('account', slug=user.slug)
        return render(request, 'register.html', {'form': form})
    

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


class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('account', kwargs={'slug': self.request.user.slug})
