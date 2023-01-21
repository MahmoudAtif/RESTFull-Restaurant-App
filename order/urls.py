from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('orders', views.OrderView)
router.register('coupons', views.CouponView)
urlpatterns = [
    # path('orders/', views.OrderView.as_view(), name='orders'),
    path('', include(router.urls))
]
