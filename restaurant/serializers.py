from rest_framework import serializers
from . import models
from datetime import datetime

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant
        fields = ['id', 'size', 'price']

class MenuItemSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True, required=False)
    class Meta:
        model=models.MenuItem
        # fields=['name', 'description', 'price', 'variant', 'variants', 'status']
        fields = '__all__'

class MenuGroupSerializer(serializers.ModelSerializer):
    items=MenuItemSerializer(read_only=True, many=True, required=False)
    class Meta:
        model=models.MenuGroup
        fields=['id','name','items']

class ResturantSerializer(serializers.ModelSerializer):
    groups=MenuGroupSerializer(read_only=True, many=True)
    status=serializers.SerializerMethodField('get_status')

    class Meta:
        model = models.Restaurant
        fields=['id', 'name', 'description', 'status', 'groups']

    def get_status(self, obj):
        weekdays = obj.days.select_related('day').all()
        dt = datetime.now()
        status = 'close'
        if weekdays.exists():
            for day in weekdays:     
                current_day = dt.strftime('%A')
                if day.day.name == current_day:
                    if dt.time() > day.opens_at and dt.time() < day.closes_at:
                        status = 'open'
                        break  
                    status='close'   
                status='close'   
        return status

    
               


