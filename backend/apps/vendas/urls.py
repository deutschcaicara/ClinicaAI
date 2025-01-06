from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendasViewSet

router = DefaultRouter()
router.register(r"vendas", VendasViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
