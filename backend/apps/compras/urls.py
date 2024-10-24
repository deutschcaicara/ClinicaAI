from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComprasViewSet

router = DefaultRouter()
router.register(r'compras', ComprasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
