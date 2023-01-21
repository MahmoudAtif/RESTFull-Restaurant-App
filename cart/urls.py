from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('carts', views.CartView)
urlpatterns = [
    # path('', views.CartView.as_view(), name='carts')
    path('', include(router.urls))
]
