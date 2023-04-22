from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.ProfileView, basename='profile')

urlpatterns = [
    path('sign-up/', views.SignUpView.as_view(), name='sign-in'),
    path('sign-in/', views.SignInView.as_view(), name='sign-up'),
    path(
        'email-verification/',
        views.EmailVerificationView.as_view(),
        name='email-verification'
    ),
    path(
        'resend-email-verification/',
        views.ResendEmailVerificationView.as_view(),
        name='resend-email-verification'
    ),
    path(
        'reset-password/',
        views.ResetPasswordView.as_view(),
        name='reset-password'
    ),
    path(
        'confirm-reset-password/',
        views.ConfirmResetPasswordView.as_view(),
        name='confirm-reset-password'
    ),
    path(
        'change-password/',
        views.ChangePasswordView.as_view(),
        name='change-password'
    ),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('', include(router.urls)),

]
