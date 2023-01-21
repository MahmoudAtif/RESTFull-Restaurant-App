from . import models
from rest_framework import serializers
from restaurant.models import Restaurant
from user.models import Customer

class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.CharField(source='get_total', read_only=True)
    class Meta:
        model = models.Cart
        fields = '__all__'
        
    # def validate(self, attrs):
    #     customer = self.context.get('request' , None).user.customer
    #     cart = models.Cart.objects.filter(restaurant_id=attrs['restaurant'], customer=customer).exists()
    #     if cart:
    #         raise serializers.ValidationError('complete last order first or remove items from basket')

    #     return super().validate(attrs)