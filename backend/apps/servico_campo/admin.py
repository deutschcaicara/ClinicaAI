from django.contrib import admin
from .models import Servico_campoModel


@admin.register(Servico_campoModel)
class Servico_campoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
