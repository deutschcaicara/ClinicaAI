from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentosViewSet

router = DefaultRouter()
router.register(r"documentos", DocumentosViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
