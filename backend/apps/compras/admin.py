from django.contrib import admin
from .models import ComprasModel

@admin.register(ComprasModel)
class ComprasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
