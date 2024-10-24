from django.contrib import admin
from .models import InventarioModel

@admin.register(InventarioModel)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
