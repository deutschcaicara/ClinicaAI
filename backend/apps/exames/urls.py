from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExameViewSet

router = DefaultRouter()
router.register(r"examess", ExameViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
