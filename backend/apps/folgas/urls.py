from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FolgasViewSet

router = DefaultRouter()
router.register(r"folgas", FolgasViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
