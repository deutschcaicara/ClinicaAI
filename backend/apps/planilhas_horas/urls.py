from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Planilhas_horasViewSet

router = DefaultRouter()
router.register(r'planilhas_horas', Planilhas_horasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
