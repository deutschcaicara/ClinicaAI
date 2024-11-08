from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Assinar_documentosViewSet

router = DefaultRouter()
router.register(r"assinar_documentos", Assinar_documentosViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
