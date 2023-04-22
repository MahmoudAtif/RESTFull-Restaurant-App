import os
import binascii
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from rest_framework.authtoken.models import Token
from . import tasks
# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_("Email Address"),
        max_length=50,
        unique=True
    )
    is_blocked = models.BooleanField(_("Blocked"), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def deactivate(self):
        self.is_active = False
        self.save()
        return True

    def activate(self):
        self.is_active = True
        self.save()
        return True

    def generate_reset_password_token(self):
        token = SecretToken.create(
            token_type="RESET_PASSWORD",
            user=self,
            expiry_hours=1
        )
        token.deactivate_previous_tokens()
        return str(token)

    def generate_email_verivication_token(self):
        token = SecretToken.create(
            token_type="EMAIL_VERIFICATION",
            user=self,
            expiry_hours=1
        )
        token.deactivate_previous_tokens()
        return str(token)

    def get_token(self):
        token, created = Token.objects.get_or_create(user=self)
        return str(token.key)


class SecretToken(TimeStampedModel):
    """SecretToken model"""

    class TokenTypes(models.TextChoices):
        RESET_PASSWORD = "RESET_PASSWORD", _("Reset Password")
        EMAIL_VERIFICATION = "EMAIL_VERIFICATION", _("Email Verification")

    key = models.CharField(blank=True, max_length=100,
                           db_index=True, verbose_name=_("Key"))
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expires At"),
    )
    lifetime = models.BooleanField(default=False)
    token_type = models.CharField(
        choices=TokenTypes.choices,
        max_length=20,
        default=TokenTypes.RESET_PASSWORD,
        verbose_name=_("Token Type"),
    )
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        db_table = "auth_secret_token"
        verbose_name = _("Secret Token")
        verbose_name_plural = _("Secret Tokens")

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(SecretToken, self).save(*args, **kwargs)

    def deactivate_previous_tokens(self):
        return (
            self.__class__.objects.filter(
                user=self.user,
                token_type=self.token_type,
            )
            .exclude(
                id=self.id,
            )
            .update(
                is_active=False,
            )
        )

    def deactivate(self):
        self.is_active = False
        self.save()
        return True

    @property
    def masked_key(self):
        value = None
        if self.key:
            value = "{0}*****{1}".format(self.key[:10], self.key[-10:])
        return value

    def generate_key(self):
        prefix = ""
        secret_key = binascii.hexlify(os.urandom(20)).decode()
        prefix = self.token_type.replace(" ", "_").lower()
        return "%s_%s" % (prefix, secret_key)

    @property
    def is_expired(self):
        if not self.is_active:
            return True

        if self.lifetime:
            return False

        if self.expires_at > timezone.now():
            return False

        return True

    @classmethod
    def create(cls, token_type, user, expiry_hours=None, lifetime=False):
        if token_type not in cls.TokenTypes.values:
            return None

        if not isinstance(expiry_hours, int) and not lifetime:
            return None

        expiry_time = timezone.now() + timedelta(hours=expiry_hours)
        return cls.objects.create(
            token_type=token_type,
            user=user,
            expires_at=expiry_time,
            lifetime=lifetime,
        )


class SendEmail(TimeStampedModel):

    class EmailTypes(models.TextChoices):
        RESET_PASSWORD = "RESET_PASSWORD", _("Reset Password")
        EMAIL_VERIFICATION = "EMAIL_VERIFICATION", _("Email Verification")
        REGULAR_EMAIL = "REGULAR_EMAIL", _('Regular Email')

    email_type = models.CharField(
        choices=EmailTypes.choices,
        max_length=20,
        default=EmailTypes.EMAIL_VERIFICATION,
        verbose_name=_("Email Type"),
    )
    email = models.EmailField(_('Email Address'), max_length=250)
    subject = models.CharField(
        verbose_name=_('Subject'),
        null=True,
        blank=True,
        max_length=100
    )
    message = models.TextField(
        verbose_name=_('Message'),
        null=True,
        blank=True,
        max_length=200
    )

    def __str__(self):
        return f'{self.email} - {self.email_type}'

    def get_user(self):
        user = User.objects.filter(email=self.email).first()
        return user

    def send_email_verification(self):
        user = self.get_user()
        if user is not None and not user.is_active:
            tasks.send_email_verification_task.delay(
                email=self.email
            )
        return None

    def send_reset_password(self):
        user = self.get_user()
        if user is not None:
            tasks.send_reset_password_task.delay(
                email=self.email
            )
        return None

    def send_regular_email(self):
        user = self.get_user()
        tasks.send_email_task.delay(
            self.subject,
            self.message,
            user.email
        )
        return True


class Favorite(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("User"),
    )
    items = models.ManyToManyField(
        "restaurant.MenuItem",
        verbose_name=_("items")
    )

    def __str__(self):
        return str(self.user)
