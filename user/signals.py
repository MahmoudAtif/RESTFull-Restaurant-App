from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.conf import settings

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            name=instance.username,
        )


@receiver(post_save, sender=User)
def create_authentication_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(
            user=instance,
        )

# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     message="{}?token={}".format(
#             instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
#             reset_password_token.key
#         )
#     send_mail('Password Reset Token', message, settings.EMAIL_HOST_USER, [reset_password_token.user.email,])