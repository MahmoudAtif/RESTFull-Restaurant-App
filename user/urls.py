from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register('customers', views.CustomersView)

urlpatterns = [
    path('api-auth/',include('rest_framework.urls')),
    path('sign-in/', views.SignInView.as_view(), name='sign_in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign_up'),
    path('email-verification/', views.EmailVerificationView.as_view(), name='email_verification'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('reset-password/', include('django_rest_passwordreset.urls')),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
    path('confirm-password/', views.PasswordConfirmView.as_view(), name='confirm_password'),
    path('',include(router.urls)),
    
]
