from . import models
from rest_framework import serializers
from restaurant.models import Restaurant, MenuItem
from django.db.models import F
from django.core.validators import MinValueValidator


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        exclude = [
            'cart',
            'restaurant'
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Cart
        exclude = [
            'user'

        ]


class AddToCartSerializer(serializers.Serializer):
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all()
    )
    item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.filter(status=True)
    )
    quantity = serializers.IntegerField(default=0, required=False)


class UpdateCartItemQuantity(serializers.Serializer):
    quantity = serializers.IntegerField(
        default=1,
        required=False,
        validators=[MinValueValidator(1)]
    )
