from django.contrib import admin
from .models import IndicacoesModel


@admin.register(IndicacoesModel)
class IndicacoesAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
