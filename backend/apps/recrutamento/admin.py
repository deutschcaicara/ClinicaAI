from django.contrib import admin
from .models import RecrutamentoModel


@admin.register(RecrutamentoModel)
class RecrutamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
