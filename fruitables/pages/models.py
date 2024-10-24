from django.db import models

class Testimonial(models.Model):
    client_name = models.CharField(max_length=50, blank=False, null=False)
    testimonial_text = models.TextField()
    stars = models.IntegerField(default=0)
    client_image = models.ImageField(upload_to='testimonial_clients_images/', null=True, blank=True)
    
    def __str__(self):
        return self.client_name
    