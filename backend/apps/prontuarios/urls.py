from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProntuarioViewSet, ProntuarioList

router = DefaultRouter()
router.register(r'prontuarios', ProntuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('prontuarios/', ProntuarioList.as_view(), name='prontuario-list'),
]