from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MensagensViewSet

router = DefaultRouter()
router.register(r"mensagens", MensagensViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
