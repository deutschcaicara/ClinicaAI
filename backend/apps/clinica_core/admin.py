from django.contrib import admin
from .models import LogSistema, Documento

@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "acao", "criado_em")
    search_fields = ("usuario__username", "acao", "detalhes")
    list_filter = ("usuario", "criado_em")

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em")
    search_fields = ("nome",)
