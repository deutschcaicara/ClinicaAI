from django.contrib import admin
from .models import Planilhas_horasModel


@admin.register(Planilhas_horasModel)
class Planilhas_horasAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
