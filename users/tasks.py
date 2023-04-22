from django.contrib.sites.models import Site
from django.urls import reverse
from celery import shared_task
from . import models
from django.conf import settings
from django.core.mail import send_mail 

def activation_url(url_name, token):
    site = Site.objects.get_current()
    domain = site.domain
    relative_url = f"{reverse(url_name)}?token={token}"
    activation_url = f'{domain}{relative_url}'
    return activation_url

@shared_task
def send_email_verification_task(email):
    user = models.User.objects.filter(email=email).first()
    token = user.generate_email_verivication_token()
    
    url_name = 'email-verification'  
    url = activation_url(url_name, token)
    subject = 'Email Activation'
    message = f'Click Here for {subject} {url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'


@shared_task
def send_reset_password_task(email):
    user = models.User.objects.filter(email=email).first()
    token = user.generate_reset_password_token()
    
    url_name = 'confirm-reset-password'
    subject = 'Reset Password'
    url = activation_url(url_name, token)
    message = f'Click Here for {subject} {url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'


@shared_task
def send_email_task(subject, message, email):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return 'Done'

