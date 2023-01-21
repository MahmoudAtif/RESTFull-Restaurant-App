from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('restaurants/', views.RestaurantView.as_view(), name='restaurants'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('items/', views.MenuItemView.as_view(), name='items'),
    path('items/<int:pk>/', views.MenuItemDetailView.as_view(), name='item_detail'),
]
