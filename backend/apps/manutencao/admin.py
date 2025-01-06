from django.contrib import admin
from .models import ManutencaoModel


@admin.register(ManutencaoModel)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
