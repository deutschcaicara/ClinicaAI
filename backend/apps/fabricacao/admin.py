from django.contrib import admin
from .models import FabricacaoModel


@admin.register(FabricacaoModel)
class FabricacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
