from django.contrib import admin
from .models import Marketing_emailModel

@admin.register(Marketing_emailModel)
class Marketing_emailAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
