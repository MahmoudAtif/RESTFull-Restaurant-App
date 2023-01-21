from rest_framework.test import APITestCase
from restaurant import views
from django.urls import reverse, resolve


class TestUrl(APITestCase):

    def test_restaurants_url(self):
        url = reverse('restaurants')
        self.assertEqual(resolve(url).func.view_class, views.RestaurantView)

    def test_restaurants_detail_url(self):
        url = reverse('restaurant_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.RestaurantDetailView)
    
    def test_items_url(self):
        url = reverse('items')
        self.assertEqual(resolve(url).func.view_class, views.MenuItemView)

    def test_items_detail_url(self):
        url = reverse('item_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, views.MenuItemDetailView)
    