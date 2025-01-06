from django.contrib import admin
from .models import FaturamentoModel


@admin.register(FaturamentoModel)
class FaturamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
