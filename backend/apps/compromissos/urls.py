from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompromissosViewSet

router = DefaultRouter()
router.register(r"compromissos", CompromissosViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
