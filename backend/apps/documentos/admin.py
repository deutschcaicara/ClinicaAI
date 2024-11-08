from django.contrib import admin
from .models import DocumentosModel


@admin.register(DocumentosModel)
class DocumentosAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
