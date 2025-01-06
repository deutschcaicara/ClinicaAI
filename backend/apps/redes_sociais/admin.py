from django.contrib import admin
from .models import Redes_sociaisModel


@admin.register(Redes_sociaisModel)
class Redes_sociaisAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
