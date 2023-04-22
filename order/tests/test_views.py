from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from order.models import Order
from restaurant.models import Restaurant


class TestView(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testemail@gmail.com',
            password='testpassword'
        )
        self.restaurant = Restaurant.objects.create(
            name='TestName',
            description='TestDesc'
        )
        self.order = Order.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            state='sddsf',
            city='sdfsdvv',
            description='dsfdsffc',
            price=0,
            total_price=0,
            status=Order.OrderStatusEnum.INITIATED
        )
        self.client.force_authenticate(self.user)

    def test_orders_list_view(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_view(self):
        url = reverse('orders-detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_order_cancel_view(self):
        url = reverse('orders-cancel', kwargs={'pk': self.order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
