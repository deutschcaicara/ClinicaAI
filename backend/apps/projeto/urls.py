from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjetoViewSet

router = DefaultRouter()
router.register(r"projeto", ProjetoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
