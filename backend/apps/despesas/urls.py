from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DespesasViewSet

router = DefaultRouter()
router.register(r"despesas", DespesasViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
