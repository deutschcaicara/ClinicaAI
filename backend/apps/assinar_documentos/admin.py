from django.contrib import admin
from .models import Assinar_documentosModel


@admin.register(Assinar_documentosModel)
class Assinar_documentosAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
