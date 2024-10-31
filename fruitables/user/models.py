from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, email='', username='', password=None):
        if not email:
            raise ValueError('Enter an email address')
        if not username:
            raise ValueError('Enter a username')
        if not password:
            raise ValueError('Enter a password')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username if username else email.split('@')[0]
        )
        user.set_password(password)
        user.save(using=self._db)  
        return user

    def create_superuser(self, email='', username='', password=None):
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True 
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    last_active_datetime = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)  

        if not self.slug:
            base_slug = slugify(self.username)
            slug = base_slug
            counter = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        super().save(*args, **kwargs)
