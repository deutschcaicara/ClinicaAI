from django.contrib import admin
from .models import CrmModel

@admin.register(CrmModel)
class CrmAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
