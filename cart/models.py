from django.db import models
from restaurant.models import AbstractModel
# Create your models here.


class Cart(AbstractModel):
    restaurant = models.ForeignKey("restaurant.Restaurant", on_delete=models.CASCADE)
    customer = models.ForeignKey('user.Customer', on_delete=models.CASCADE, related_name='carts')
    item = models.ForeignKey('restaurant.MenuItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(blank=True, max_digits=5, decimal_places=2) 
    
    @property
    def get_total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return str(self.item)
    