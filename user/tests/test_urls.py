from rest_framework.test import APITestCase
from django.urls import reverse, resolve
from user import views 

class TestUrl(APITestCase):

    def test_sign_in_url(self):
        url = reverse('sign_in')
        self.assertEqual(resolve(url).func.view_class, views.SignInView)

    def test_sign_up_url(self):
        url = reverse('sign_up')
        self.assertEqual(resolve(url).func.view_class, views.SignUpView)

    def test_email_verification_url(self):
        url = reverse('email_verification')
        self.assertEqual(resolve(url).func.view_class, views.EmailVerificationView)

    def test_change_password_url(self):
        url = reverse('change_password')
        self.assertEqual(resolve(url).func.view_class, views.ChangePasswordView)

    def test_reset_password_url(self):
        url = reverse('reset_password')
        self.assertEqual(resolve(url).func.view_class, views.PasswordResetView)

    def test_confirm_password_url(self):
        url = reverse('confirm_password')
        self.assertEqual(resolve(url).func.view_class, views.PasswordConfirmView)