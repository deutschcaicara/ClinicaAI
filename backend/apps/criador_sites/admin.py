from django.contrib import admin
from .models import Criador_sitesModel

@admin.register(Criador_sitesModel)
class Criador_sitesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
