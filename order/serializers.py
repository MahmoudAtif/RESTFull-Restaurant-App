from . import models
from rest_framework import serializers
from cart.models import Cart
from rest_framework.validators import ValidationError

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['id', 'item', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = models.Order
        fields = '__all__'



class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = '__all__'