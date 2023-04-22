from django.db import models
from restaurant.models import AbstractModel
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.core.validators import MinValueValidator
from django.db.models import F
from django.db.models import Sum
from django.db.models.functions import Coalesce, Cast
from math import *
# Create your models here.


class Cart(AbstractModel):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    total = models.FloatField(
        default=0,
        verbose_name=_("Total"),
    )
    sub_total = models.FloatField(
        default=0,
        verbose_name=_("Sub total"),
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.id:
            self._recalculate_cart()

    @property
    def get_total(self):
        return self.price * self.quantity

    def clear(self):
        self.total = 0
        self.sub_total = 0
        self.items.all().delete()
        self.save()
        return True

    def _calculate_sub_total(self):
        total = self.items.aggregate(
            sum=Coalesce(
                Sum(F('item__price') * F('quantity')),
                0,
                output_field=models.FloatField()
            )
        )['sum']
        self.sub_total = round(total, 2)
        self.total = round(total, 2)
        return self.sub_total, total

    def _recalculate_cart(self):
        self._calculate_sub_total()
        self.save()

    def __str__(self):
        return str(self.user)


class CartItem(AbstractModel):
    cart = models.ForeignKey(
        "cart.Cart",
        verbose_name=_("Cart"),
        related_name='items',
        on_delete=models.CASCADE
    )
    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        verbose_name=_("Restaurant"),
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        'restaurant.MenuItem',
        validators=[
            MinValueValidator(1),
        ],
        verbose_name=_("Item"),
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.cart} - {self.restaurant} - {self.item}'
