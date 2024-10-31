# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .utils import Email

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    def clean_email(self):
        super().clean_username()
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter an email address')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        if not Email.is_valid_email(email):
            raise forms.ValidationError('Please enter a valid email address')
        return email

