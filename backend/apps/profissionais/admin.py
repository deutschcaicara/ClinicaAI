from django.contrib import admin
from .models import Profissional, Especialidade, Disponibilidade, RegistroHorasTrabalhadas

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'registro_conselho', 'conselho', 'email']
    search_fields = ['nome_completo', 'registro_conselho']

@admin.register(Especialidade)
class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

@admin.register(Disponibilidade)
class DisponibilidadeAdmin(admin.ModelAdmin):
    list_display = ['profissional', 'dia', 'horario_inicio', 'horario_fim']
    list_filter = ['dia', 'disponivel']

@admin.register(RegistroHorasTrabalhadas)
class RegistroHorasTrabalhadasAdmin(admin.ModelAdmin):
    list_display = ['profissional', 'dia', 'horas_trabalhadas']
    list_filter = ['dia']
