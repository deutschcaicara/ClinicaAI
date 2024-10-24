from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Recursos_humanosViewSet

router = DefaultRouter()
router.register(r'recursos_humanos', Recursos_humanosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
