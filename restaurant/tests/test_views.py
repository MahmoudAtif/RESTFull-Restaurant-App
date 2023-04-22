from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from rest_framework.authtoken.models import Token
from restaurant.models import Restaurant, MenuGroup, MenuItem


class TestView(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='TestName',
            description='TestDesc'
        )
        self.group = MenuGroup.objects.create(
            restaurant=self.restaurant,
            name='TestGroup'
        )
        self.item = MenuItem.objects.create(
            restaurant=self.restaurant,
            group=self.group,
            name='TestItem',
            variant=MenuItem.ItemVariant.NO_SIZE,
            price=100,
            status=True
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='testpassword'
        )

    def test_restaurants_list_view(self):
        url = reverse('restaurants-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], 'SUCCESS')

    def test_restaurant_retrieve_view(self):
        url = reverse('restaurants-detail', kwargs={'pk': self.restaurant.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_favorite_view(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            'restaurants-favorite',
            kwargs={
                'pk': self.restaurant.pk,
                'item_pk': self.item.pk
            }
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_favorite_view(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            'restaurants-unfavorite',
            kwargs={
                'pk': self.restaurant.pk,
                'item_pk': self.item.pk
            }
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
