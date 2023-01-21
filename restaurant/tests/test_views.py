from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from restaurant.models import Restaurant, MenuGroup, Size, Variant, MenuItem

class TestView(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test', email='test@gmail.com')
        self.token = Token.objects.get(user=self.user)
        # Token Authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.restaurant = Restaurant.objects.create(name='test', description='test')
        self.group = MenuGroup.objects.create(restaurant=self.restaurant, name='testgroup')
        self.item = MenuItem.objects.create(restaurant=self.restaurant, group=self.group, name='testitem', variant=1, description='itemdescription', price=100)
        self.size = Size.objects.create(name='testsize')
        self.variant = Variant.objects.create(item=self.item, size=self.size, price=self.item.price) 
    
    def test_restaurants_view(self):
        url = reverse('restaurants')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurants_post_view(self):
        url = reverse('restaurants')
        data = {
            'name':'newRestaurant',
            'description':'newRestaurantDescription'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_restaurants_detail_view(self):
        url = reverse('restaurant_detail', args=[self.restaurant.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_restaurants_detail_put_view(self):
        url = reverse('restaurant_detail', args=[self.restaurant.pk])
        data = {
            'name':'newRestaurant',
            'description':'newRestaurantDescription'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurants_detail_delete_view(self):
        url = reverse('restaurant_detail', args=[self.restaurant.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)    
    
    def test_items_view(self):
        url = reverse('items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_items_post_view(self):
        url = reverse('items')

        data = {
            "restaurant": self.restaurant.id,
            "group": self.group.id,
            "name": 'newItem',
            "variant": self.variant.id,
            "description": "testdesc",
            "status": True,
            "price": 100
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_item_detail_put_view(self):
        url = reverse('item_detail', args=[self.item.pk])
        data = {
            "restaurant": self.restaurant.id,
            "group": self.group.id,
            "name": 'newItem2',
            "variant": self.variant.id,
            "description": "testdesc",
            "status": True,
            "price": 100
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restaurants_detail_delete_view(self):
        url = reverse('item_detail', args=[self.item.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)   