from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.generics import ListCreateAPIView
# Create your views here.

class OrderView(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class=serializers.OrderSerializer
    throttle_classes = ()
    permission_classes = ()

class CouponView(viewsets.ModelViewSet):
    queryset = models.Coupon.objects.all()
    serializer_class=serializers.CouponSerializer
    throttle_classes = ()


