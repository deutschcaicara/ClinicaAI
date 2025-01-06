from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Redes_sociaisViewSet

router = DefaultRouter()
router.register(r"redes_sociais", Redes_sociaisViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
