from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    phone=PhoneNumberField(null=True, blank=True)
    image=models.ImageField(upload_to='customer_images', null=True, blank=True)
    
    def __str__(self):
        return self.name
