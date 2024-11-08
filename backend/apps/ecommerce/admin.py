from django.contrib import admin
from .models import EcommerceModel


@admin.register(EcommerceModel)
class EcommerceAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
