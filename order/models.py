from django.db import models
from restaurant.models import AbstractModel
# Create your models here.


class Order(AbstractModel):

    class OrderStatusEnum(models.IntegerChoices):
        INITIATED = 0, "Initiated"
        CONFIRMED = 1, "Confirmed"
        DELIVERED = 2, "Delivered"

    customer = models.ForeignKey('user.Customer', on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey("restaurant.Restaurant", on_delete=models.CASCADE,related_name='orders')
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    total_price = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    status = models.IntegerField(choices=OrderStatusEnum.choices)
    is_paid = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.price
        super(Order,self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer} | {self.restaurant}'


class OrderItem(AbstractModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey("restaurant.MenuItem",on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.order} | {self.item}'



class Coupon(AbstractModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='coupon')
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=False)

    @property
    def make_discount(self):
        total = self.order.price-(self.order.price * self.discount/100)
        return total
    
    def save(self, *args, **kwargs):
        self.order.total_price = self.make_discount
        self.order.save()
        super(Coupon,self).save(*args, **kwargs)

    def __str__(self):
        return self.code