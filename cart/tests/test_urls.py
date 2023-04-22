from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from cart import views


class TestUrl(APITestCase):

    def test_cart_list_url(self):
        url = reverse('cart-list')
        view = resolve(url).func.cls
        self.assertEqual(view, views.CartViewset)

    def test_add_to_cart_url(self):
        url = reverse('cart-add')
        view = resolve(url).func.cls
        self.assertEqual(view, views.CartViewset)

    def test_remove_from_cart_url(self):
        url = reverse('cart-remove', kwargs={'pk': 1})
        view = resolve(url).func.cls
        self.assertEqual(view, views.CartViewset)

    def test_update_cart_quantity_url(self):
        url = reverse('cart-update-quantity', kwargs={'pk': 1})
        view = resolve(url).func.cls
        self.assertEqual(view, views.CartViewset)

    def test_checkout_url(self):
        url = reverse('cart-checkout')
        view = resolve(url).func.cls
        self.assertEqual(view, views.CartViewset)
        
    def test_clear_cart_url(self):
        url = reverse('cart-clear')
        view = resolve(url).func.cls
        self.assertEqual(view, views.CartViewset)