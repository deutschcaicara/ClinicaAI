from django.contrib import admin
from .models import CompromissosModel


@admin.register(CompromissosModel)
class CompromissosAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
