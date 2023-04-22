from rest_framework import serializers
from . import models


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant
        fields = ['id', 'size', 'price']


class MenuItemSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = models.MenuItem
        fields = '__all__'


class MenuGroupSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(read_only=True, many=True, required=False,)

    class Meta:
        model = models.MenuGroup
        fields = ['id', 'name', 'items']


class ResturantSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status')
    rate = serializers.FloatField()

    class Meta:
        model = models.Restaurant
        fields = ['id', 'name', 'description', 'status', 'rate']


class ResturantDeatilSerializer(serializers.ModelSerializer):
    groups = MenuGroupSerializer(read_only=True, many=True)
    status = serializers.CharField(source='get_status', read_only=True)
    rate = serializers.FloatField()

    class Meta:
        model = models.Restaurant
        fields = ['id', 'name', 'description', 'status', 'groups', 'rate']


class ReviewInputsSerializer(serializers.Serializer):
    comment = serializers.CharField()
    rating = serializers.FloatField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
