from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlmViewSet

router = DefaultRouter()
router.register(r"plm", PlmViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
