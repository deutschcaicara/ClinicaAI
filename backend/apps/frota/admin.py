from django.contrib import admin
from .models import FrotaModel


@admin.register(FrotaModel)
class FrotaAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
