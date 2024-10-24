from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clinicaai.paciente.models.paciente import Paciente  # Remover temporariamente modelos não criados ainda

class Command(BaseCommand):
    help = 'Cria grupos de usuários e atribui permissões automaticamente'

    def handle(self, *args, **kwargs):
        # Definir Grupos
        grupos = [
            'Recepcao', 'Medicos', 'Enfermeiros', 'Psicologos', 
            'Administracao', 'AdminCompleto', 'Financeiro', 'TI', 
            'GerenteQualidade', 'SupervisoresSetor', 'ProfissionaisReabilitacao', 'SupervisoresFinanceiros', 'FamiliaresAutorizados'
        ]

        # Criar Grupos
        for grupo in grupos:
            novo_grupo, criado = Group.objects.get_or_create(name=grupo)
            if criado:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{grupo}" criado com sucesso'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{grupo}" já existe'))

        # Definir Permissões para cada grupo
        # Grupo Recepção
        grupo_recepcao = Group.objects.get(name='Recepcao')
        permissoes_recepcao = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_recepcao.permissions.set(permissoes_recepcao)

        # Grupo Médicos
        grupo_medicos = Group.objects.get(name='Medicos')
        permissoes_medicos = [
            Permission.objects.get(codename='view_paciente'),
            Permission.objects.get(codename='change_paciente'),
        ]
        grupo_medicos.permissions.set(permissoes_medicos)

        # Grupo Enfermeiros
        grupo_enfermeiros = Group.objects.get(name='Enfermeiros')
        permissoes_enfermeiros = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_enfermeiros.permissions.set(permissoes_enfermeiros)

        # Grupo Psicólogos
        grupo_psicologos = Group.objects.get(name='Psicologos')
        permissoes_psicologos = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_psicologos.permissions.set(permissoes_psicologos)

        # Grupo Administração/Vendas
        grupo_administracao = Group.objects.get(name='Administracao')
        permissoes_administracao = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_administracao.permissions.set(permissoes_administracao)

        # Grupo Admin Completo
        grupo_admin = Group.objects.get(name='AdminCompleto')
        permissoes_admin = Permission.objects.all()
        grupo_admin.permissions.set(permissoes_admin)

        # Grupo Financeiro
        grupo_financeiro = Group.objects.get(name='Financeiro')
        permissoes_financeiro = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_financeiro.permissions.set(permissoes_financeiro)

        # Grupo TI/DevOps
        grupo_ti = Group.objects.get(name='TI')
        permissoes_ti = [
            Permission.objects.get(codename='view_paciente'),
            Permission.objects.get(codename='add_paciente'),
            Permission.objects.get(codename='change_paciente'),
            Permission.objects.get(codename='delete_paciente'),
        ]
        grupo_ti.permissions.set(permissoes_ti)

        # Grupo Gerente de Qualidade
        grupo_gerente_qualidade = Group.objects.get(name='GerenteQualidade')
        permissoes_gerente_qualidade = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_gerente_qualidade.permissions.set(permissoes_gerente_qualidade)

        # Grupo Supervisores de Setor
        grupo_supervisores = Group.objects.get(name='SupervisoresSetor')
        permissoes_supervisores = [
            Permission.objects.get(codename='view_paciente'),
            Permission.objects.get(codename='change_paciente'),
        ]
        grupo_supervisores.permissions.set(permissoes_supervisores)

        # Grupo Profissionais de Reabilitação
        grupo_reabilitacao = Group.objects.get(name='ProfissionaisReabilitacao')
        permissoes_reabilitacao = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_reabilitacao.permissions.set(permissoes_reabilitacao)

        # Grupo Supervisores Financeiros
        grupo_supervisores_financeiros = Group.objects.get(name='SupervisoresFinanceiros')
        permissoes_supervisores_financeiros = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_supervisores_financeiros.permissions.set(permissoes_supervisores_financeiros)

        # Grupo Familiares Autorizados
        grupo_familiares = Group.objects.get(name='FamiliaresAutorizados')
        permissoes_familiares = [
            Permission.objects.get(codename='view_paciente'),
        ]
        grupo_familiares.permissions.set(permissoes_familiares)

        self.stdout.write(self.style.SUCCESS('Grupos e permissões configurados com sucesso'))
