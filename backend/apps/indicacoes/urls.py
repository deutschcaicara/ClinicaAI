from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndicacoesViewSet

router = DefaultRouter()
router.register(r'indicacoes', IndicacoesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
