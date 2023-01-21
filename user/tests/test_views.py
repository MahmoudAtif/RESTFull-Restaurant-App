from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestView(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test',password='test',email='test@gmail.com')
        self.token = Token.objects.get(user=self.user)
        # Token Authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    def test_sign_in_view(self):
        url = reverse('sign_in')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_sign_in_post_view(self):
        url = reverse('sign_in')
        data = {
            'username_or_email':'test',
            'password':'test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.token.key)
    

    def test_sign_up_view(self):
        url = reverse('sign_up')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_sign_up_post_view(self):
        url = reverse('sign_up')
        data = {
            'username':'test1',
            'email':'test1@gmail.com',
            'password':'test123456789'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_email_verification_view(self):
        url = "{}?token={}".format(
            reverse('email_verification'),
            self.token.key
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_view(self):
        url = reverse('change_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_change_password_post_view(self):
        url = reverse('change_password')
        data = {
            'old_password':'test',
            'new_password':'test123456789'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_view(self):
        url = reverse('reset_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_reset_password_post_view(self):
        url = reverse('reset_password')
        data = {
            'email':self.user.email
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    
    def test_confirm_password_view(self):
        url = "{}?token={}".format(
            reverse('confirm_password'),
            self.token.key
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_confirm_password_post_view(self):
        url = "{}?token={}".format(
            reverse('confirm_password'),
            self.token.key
        )
        data = {
            'token':self.token.key,
            'new_password':self.user.email
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 