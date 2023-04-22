from rest_framework.test import APITestCase
from restaurant import views
from django.urls import reverse, resolve


class TestUrl(APITestCase):

    def test_restaurants_list_url(self):
        url = reverse('restaurants-list')
        view = resolve(url).func.cls
        self.assertEqual(view, views.RestaurantViewSet)

    def test_restaurant_detail_url(self):
        url = reverse('restaurants-detail', kwargs={'pk': 1})
        view = resolve(url).func.cls
        self.assertEqual(view, views.RestaurantViewSet)

    def test_add_favorite_url(self):
        url = reverse(
            'restaurants-favorite',
            kwargs={
                'pk': 1,
                'item_pk': 1
            }
        )
        view = resolve(url).func.cls
        self.assertEqual(view, views.RestaurantViewSet)
