from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register('cart', views.CartViewset, basename='cart')

urlpatterns = [
    path('', include(routers.urls)),
]
