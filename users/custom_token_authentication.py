from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        """CustomTokenAuthentication to restrict blocked users"""
        user, token = super().authenticate_credentials(key)

        if user.is_blocked:
            raise AuthenticationFailed(
                _('User has been temporarily blocked due to violating the rules.')
            )
        return user, token
