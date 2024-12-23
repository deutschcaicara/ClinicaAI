from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssinaturaViewSet

router = DefaultRouter()
router.register(r"assinaturas", AssinaturaViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
