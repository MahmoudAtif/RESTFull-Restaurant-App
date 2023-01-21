from django.shortcuts import render
from rest_framework.views import APIView
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

def index(request):
    return render(request, 'index.html')

class RestaurantView(APIView):
    
    throttle_classes=()
    
    def get(self, request):
        queryset = models.Restaurant.objects.all()
        serializer = serializers.ResturantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.ResturantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RestaurantDetailView(APIView):
   
    throttle_classes=()

    def get_object(self, pk):
        try:
            obj = models.Restaurant.objects.get(pk=pk)
            return obj
        except:
            return None

    def get(self, request, pk):
        restaurant = self.get_object(pk)
        serializer = serializers.ResturantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer = serializers.ResturantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        restaurant = self.get_object(pk)
        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuItemView(APIView):
   
    throttle_classes=()

    def get(self, request):
        queryset = models.MenuItem.objects.all()
        serializer = serializers.MenuItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuItemDetailView(APIView):
    
    throttle_classes=()

    def get_object(self, pk):
        try:
            obj = models.MenuItem.objects.get(pk=pk)
            return obj
        except:
            return None

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = serializers.MenuItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer = serializers.MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)