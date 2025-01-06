from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecrutamentoViewSet

router = DefaultRouter()
router.register(r"recrutamento", RecrutamentoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
