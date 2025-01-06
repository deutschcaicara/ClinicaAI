from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvaliacoesViewSet

router = DefaultRouter()
router.register(r"avaliacoes", AvaliacoesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
