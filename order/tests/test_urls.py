from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from order.models import Order, OrderItem
from order import views


class TestUrl(APITestCase):

    def test_order_list_url(self):
        url = reverse('orders-list')
        view = resolve(url).func.cls
        self.assertEqual(view, views.OrderViewSet)

    def test_order_detail_url(self):
        url = reverse('orders-detail', kwargs={'pk': 1})
        view = resolve(url).func.cls
        self.assertEqual(view, views.OrderViewSet)

    def test_cancel_url(self):
        url = reverse('orders-cancel', kwargs={'pk': 1})
        view = resolve(url).func.cls
        self.assertEqual(view, views.OrderViewSet)
