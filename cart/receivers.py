from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cart

# @receiver(pre_save, sender=Cart)
# def add_price_for_cart_item(sender, instance, **kwargs):
#     """ set data for price field """
#     instance.price = instance.item.price
