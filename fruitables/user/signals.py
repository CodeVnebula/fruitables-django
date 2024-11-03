from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import User
from order.models import Cart

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)  
