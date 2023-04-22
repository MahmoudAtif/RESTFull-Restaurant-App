from django.contrib.auth.backends import ModelBackend, BaseBackend
from .models import User
from django.db.models import Q


class CustomModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(
            Q(username=username) |
            Q(email=username)
        ).first()

        if user is not None and user.check_password(password):
            return user

        return None
