from django.contrib import admin
from .models import MensagensModel


@admin.register(MensagensModel)
class MensagensAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
