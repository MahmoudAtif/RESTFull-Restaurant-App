from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import User, SendEmail
from rest_framework.authtoken.models import Token
from django.core import exceptions


@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(
            user=instance
        )

    return None


@receiver(post_save, sender=User)
def send_email_verification_receiver(sender, instance, created, **kwargs):
    if not instance.is_active:
        SendEmail.objects.create(
            email_type='EMAIL_VERIFICATION',
            email=instance.email
        )
    return True


@receiver(pre_save, sender=SendEmail)
def send_email_based_type_receiver(sender, instance, **kwargs):
    if instance.email_type == 'RESET_PASSWORD':
        return instance.send_reset_password()

    elif instance.email_type == 'REGULAR_EMAIL':
        if not instance.subject and not instance.message:
            raise exceptions.ValidationError(
                "can't save without subject and message"
            )
        return instance.send_regular_email()

    else:
        return instance.send_email_verification()
