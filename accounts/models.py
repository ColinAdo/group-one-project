from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

def user_directory_path(instance, filename):
    return "profile/{0}/{1}".format(instance.username, filename)

def vendor_directory_path(instance, filename):
    return "Vendor/{0}/{1}".format(instance.name, filename)

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(max_length=200, default="profile.png", upload_to=user_directory_path)

    def __str__(self):
        return self.username
    
class Vendor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=vendor_directory_path, default='venders.jpg')
    description = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=100, default='(+254) 123 456 678')
    address = models.CharField(max_length=100, default='P.0 Box Nairobi')
    warranty_period = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Venders'

    def __str__(self):
        return self.name
