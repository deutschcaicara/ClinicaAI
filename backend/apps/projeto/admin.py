from django.contrib import admin
from .models import ProjetoModel


@admin.register(ProjetoModel)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
