from django.contrib import admin
from .models import Chat_ao_vivoModel


@admin.register(Chat_ao_vivoModel)
class Chat_ao_vivoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
