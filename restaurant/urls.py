from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register('restaurants', views.RestaurantViewSet, basename='restaurants')

urlpatterns = [
    path('', include(routers.urls))
]
