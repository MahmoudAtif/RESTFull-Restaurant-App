from rest_framework.throttling import AnonRateThrottle


class CustomeResetPassswordThruttle(AnonRateThrottle):
    scope = 'reset_password'