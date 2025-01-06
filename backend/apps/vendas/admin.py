from django.contrib import admin
from .models import VendasModel


@admin.register(VendasModel)
class VendasAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
