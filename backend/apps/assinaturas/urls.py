from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssinaturasViewSet

router = DefaultRouter()
router.register(r'assinaturas', AssinaturasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
