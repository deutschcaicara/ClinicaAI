from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Servico_campoViewSet

router = DefaultRouter()
router.register(r'servico_campo', Servico_campoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
