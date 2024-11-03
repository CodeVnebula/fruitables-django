# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User
from .utils import Email

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': 'Please enter your username.'
        }
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email',
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': 'Please enter your email address.'
        }
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'class': 'form-control',
                'id': 'id_password1' 
            }
        ),
        error_messages={
            'required': 'Please enter your password.'
        }
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
                'class': 'form-control',
                'id': 'id_password2' 
            }
        ),
        error_messages={
            'required': 'Please confirm your password.'
        }
    )        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Please enter an email address.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        if not Email.is_valid_email(email):
            raise ValidationError('Please enter a valid email address.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your username',
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': 'Please enter your username.'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'class': 'form-control',
                'id': 'id_password' 
            }
        ),
        error_messages={
            'required': 'Please enter your password.'
        }
    )
