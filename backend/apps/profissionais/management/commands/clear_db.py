from django.core.management.base import BaseCommand
from apps.profissionais.models import Profissional, Especialidade
from apps.pacientes.models import Paciente
from apps.exames.models import Exame
from apps.agendamentos.models import Agendamento
from apps.prontuarios.models import Prontuario
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Apaga todos os dados do banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write("Apagando todos os dados do banco de dados...\n")

        # Apagar os registros em ordem para evitar erros de chaves estrangeiras
        Agendamento.objects.all().delete()
        Prontuario.objects.all().delete()
        Exame.objects.all().delete()
        Paciente.objects.all().delete()
        Profissional.objects.all().delete()
        Especialidade.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()  # Preserva o superusuário

        self.stdout.write(self.style.SUCCESS("Todos os dados foram apagados com sucesso!"))
