from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaturamentoViewSet

router = DefaultRouter()
router.register(r"faturamento", FaturamentoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
