from . import models
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        exclude = [
            'order'
        ]


class OrderSerializer(serializers.ModelSerializer):
    restaurant = serializers.StringRelatedField()

    class Meta:
        model = models.Order
        fields = [
            'id',
            'restaurant',
            'status'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = models.Order.OrderStatusEnum(
            instance.status
        ).label
        return representation


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        exclude = [
            'user'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = models.Order.OrderStatusEnum(
            instance.status
        ).label
        return representation


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = '__all__'


class CheckoutInputSerializer(serializers.Serializer):
    state = serializers.CharField()
    city = serializers.CharField()
    description = serializers.CharField()
