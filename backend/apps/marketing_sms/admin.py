from django.contrib import admin
from .models import Marketing_smsModel

@admin.register(Marketing_smsModel)
class Marketing_smsAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_em', 'atualizado_em')
