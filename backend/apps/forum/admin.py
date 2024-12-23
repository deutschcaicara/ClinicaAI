from django.contrib import admin
from .models import ForumModel


@admin.register(ForumModel)
class ForumAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "atualizado_em")
