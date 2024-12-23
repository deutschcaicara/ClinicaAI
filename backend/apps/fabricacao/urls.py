from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FabricacaoViewSet

router = DefaultRouter()
router.register(r"fabricacao", FabricacaoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
