from django.contrib import admin
from .models import Recursos_humanosModel


@admin.register(Recursos_humanosModel)
class Recursos_humanosAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
