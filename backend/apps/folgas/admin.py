from django.contrib import admin
from .models import FolgasModel

@admin.register(FolgasModel)
class FolgasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
