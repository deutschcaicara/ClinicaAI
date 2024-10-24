# Arquivo: /mnt/dados/clinicaai/pacientes/urls.py

from django.urls import path
from .views import ConsultaAPIView, ExameAPIView

urlpatterns = [
    path('consultas/', ConsultaAPIView.as_view(), name='consultas'),
    path('exames/', ExameAPIView.as_view(), name='exames'),
]
