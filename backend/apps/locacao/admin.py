from django.contrib import admin
from .models import LocacaoModel

@admin.register(LocacaoModel)
class LocacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
