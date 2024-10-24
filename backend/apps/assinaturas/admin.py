from django.contrib import admin
from .models import AssinaturasModel

@admin.register(AssinaturasModel)
class AssinaturasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
