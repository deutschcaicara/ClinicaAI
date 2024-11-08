from django.contrib import admin
from .models import ElearningModel


@admin.register(ElearningModel)
class ElearningAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
