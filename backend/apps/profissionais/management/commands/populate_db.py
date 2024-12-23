import random
from django.core.management.base import BaseCommand
from apps.profissionais.models import Profissional, Especialidade
from apps.pacientes.models import Paciente
from apps.exames.models import Exame
from apps.agendamentos.models import Agendamento
from apps.prontuarios.models import Prontuario
from django.contrib.auth import get_user_model
from datetime import date, timedelta, datetime
from faker import Faker
from django.utils import timezone

User = get_user_model()
fake = Faker('pt_BR')

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste mais realistas'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populando banco de dados...\n")
        
        # Criando usuários de exemplo
        users = []
        for i in range(1, 6):
            username = f"usuario{i}"
            user, created = User.objects.get_or_create(username=username, defaults={'password': f"senha123{i}"})
            users.append(user)

        # Criando especialidades
        especialidades_nomes = [
            "Cardiologia", "Dermatologia", "Ortopedia", "Neurologia", "Pediatria"
        ]
        especialidades = []
        for especialidade_nome in especialidades_nomes:
            especialidade, created = Especialidade.objects.get_or_create(nome=especialidade_nome)
            especialidades.append(especialidade)

        # Criando profissionais de saúde
        for i in range(1, 6):
            cpf = self.gerar_cpf_unico()
            registro_conselho = f"CRP-{random.randint(1000, 9999)}"  # Registro único
            profissional, created = Profissional.objects.get_or_create(
                usuario=random.choice(users),
                defaults={
                    'nome_completo': fake.name(),
                    'cpf': cpf,
                    'registro_conselho': registro_conselho,
                    'conselho': "CRM",
                    'telefone': f"1199999{i:04d}",
                    'email': f"profissional{i}@clinicaai.com",
                    'endereco': f"Rua Exemplo, {i}",
                    'tipo_contratacao': random.choice(["CLT", "PJ", "Freelancer"]),
                    'horario_atendimento_inicio': "08:00",
                    'horario_atendimento_fim': "17:00",
                    'dias_atendimento': random.choice(["Segunda a Sexta", "Segunda a Sábado"])
                }
            )
            if created:
                profissional.especialidades.set([random.choice(especialidades)])

        # Criando pacientes
        for i in range(1, 11):
            username = f"paciente{i}"
            user, created = User.objects.get_or_create(username=username, defaults={'password': f"senha123{i}"})
            if hasattr(user, 'paciente') or hasattr(user, 'profissional'):
                continue  # Pule usuários já associados
            cpf = self.gerar_cpf_unico()
            Paciente.objects.get_or_create(
                cpf=cpf,
                defaults={
                    'nome_completo': fake.name(),
                    'data_nascimento': date(1980, 1, 1) + timedelta(days=random.randint(0, 15000)),
                    'telefone_celular': f"99999{random.randint(1000, 9999)}",
                    'email': f"paciente{i}@teste.com"
                }
            )

        # Criando exames
        pacientes = Paciente.objects.all()
        profissionais = Profissional.objects.all()
        exames_nomes = [
            "Exame de sangue", "Raio X", "Ultrassom", "ECG", "Teste de glicose"
        ]
        exames = []
        for exame_nome in exames_nomes:
            paciente = random.choice(pacientes)
            profissional = random.choice(profissionais)
            exame, created = Exame.objects.get_or_create(
                tipo_exame=exame_nome,
                paciente=paciente,
                profissional_solicitante=profissional,
                defaults={
                    'observacoes': f"Descrição do {exame_nome}",
                    'data_solicitacao': date.today()
                }
            )
            exames.append(exame)

        # Criando agendamentos sem conflitos
        for i in range(1, 11):
            profissional = random.choice(profissionais)
            data_agendamento = date.today() + timedelta(days=random.randint(1, 30))
            horario_inicio = random.randint(8, 16)
            horario_fim = horario_inicio + 1  # Garante que o horário de fim seja posterior

            if not Agendamento.objects.filter(
                profissional=profissional,
                data_agendamento=data_agendamento,
                horario_inicio=f"{horario_inicio}:00"
            ).exists():
                Agendamento.objects.create(
                    paciente=random.choice(pacientes),
                    profissional=profissional,
                    data_agendamento=data_agendamento,
                    horario_inicio=f"{horario_inicio}:00",
                    horario_fim=f"{horario_fim}:00",
                    tipo_consulta=random.choice(["Consulta de rotina", "Retorno", "Urgência"])
                )

        # Criando prontuários
        agendamentos = Agendamento.objects.all()
        for agendamento in agendamentos:
            Prontuario.objects.update_or_create(
                paciente=agendamento.paciente,
                profissional_responsavel=agendamento.profissional,
                data_atendimento=datetime.combine(agendamento.data_agendamento, datetime.min.time(), tzinfo=timezone.utc),
                defaults={
                    'queixa_principal': "Diagnóstico fictício e tratamento sugerido."
                }
            )

        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))

    def gerar_cpf_unico(self):
        while True:
            cpf = f"{random.randint(10000000000, 99999999999)}"
            if not Profissional.objects.filter(cpf=cpf).exists() and not Paciente.objects.filter(cpf=cpf).exists():
                return cpf
