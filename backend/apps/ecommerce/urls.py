from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EcommerceViewSet

router = DefaultRouter()
router.register(r'ecommerce', EcommerceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
