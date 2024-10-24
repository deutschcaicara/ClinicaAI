from django.contrib import admin
from .models import DespesasModel

@admin.register(DespesasModel)
class DespesasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
