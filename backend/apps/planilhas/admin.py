from django.contrib import admin
from .models import PlanilhasModel


@admin.register(PlanilhasModel)
class PlanilhasAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
