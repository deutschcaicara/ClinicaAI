# Módulo Profissionais - URLs (urls.py)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"especialidades", views.EspecialidadeViewSet)
router.register(r"profissionais", views.ProfissionalViewSet)
router.register(r"disponibilidades", views.DisponibilidadeViewSet)
router.register(r"horas_trabalhadas", views.RegistroHorasTrabalhadasViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
