from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Criador_sitesViewSet

router = DefaultRouter()
router.register(r"criador_sites", Criador_sitesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
