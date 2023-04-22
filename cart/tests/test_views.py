from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status
from django.urls import reverse
from cart.models import Cart, CartItem
from restaurant.models import Restaurant, MenuGroup, MenuItem
from rest_framework.authtoken.models import Token


class TestView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Testuser2',
            email='Testemail2@gmail.com',
            password='testpassword'
        )
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
        self.cart, created = Cart.objects.get_or_create(
            user=self.user,
        )
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            restaurant=self.restaurant,
            item=self.item,
            quantity=1
        )
        self.client.force_authenticate(self.user)

    def test_cart_list_view(self):
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart_view(self):
        url = reverse('cart-add')
        data = {
            'restaurant': self.restaurant.pk,
            'item': self.item.pk,
            'quantity': 1
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_cart_view(self):
        url = reverse('cart-remove', kwargs={'pk': self.cart_item.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cart_quantity_View(self):
        url = reverse('cart-update-quantity', kwargs={'pk': self.cart_item.pk})
        data = {
            'quantity': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_checkout_view(self):
        url = reverse('cart-checkout')
        data = {
            "state": "dfhnhndf",
            "city": "dfddfcdsff",
            "description": "Any Desc"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clear_cart_View(self):
        url = reverse('cart-clear')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
