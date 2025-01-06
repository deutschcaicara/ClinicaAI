from django.contrib import admin
from .models import Prontuario

class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'data_atendimento', 'prescricao', 'profissional_responsavel')

admin.site.register(Prontuario, ProntuarioAdmin)

from .models import Anamnese

admin.site.register(Anamnese)
