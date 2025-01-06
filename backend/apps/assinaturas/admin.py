from django.contrib import admin
from .models import Assinatura


@admin.register(Assinatura)
class AssinaturasAdmin(admin.ModelAdmin):
    list_display = ("documento", "assinante", "data_assinatura", "validade_assinatura")
