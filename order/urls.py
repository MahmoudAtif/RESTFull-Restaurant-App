from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('my-orders', views.OrderViewSet, basename='orders')
# router.register('coupons', views.CouponView)
urlpatterns = [
    path('', include(router.urls))
]
