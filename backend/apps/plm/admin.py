from django.contrib import admin
from .models import PlmModel

@admin.register(PlmModel)
class PlmAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
