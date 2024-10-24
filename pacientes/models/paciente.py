from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    # Dados Pessoais
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Permitindo nulo para evitar erro em registros existentes
    endereco = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    data_nascimento = models.DateField(default=timezone.now, null=True, blank=True)  # Permitindo valor padrão e valores nulos
    contato_emergencia = models.CharField(max_length=255, default='Sem contato', null=True, blank=True)
    telefone_emergencia = models.CharField(max_length=20, null=True, blank=True)

    # Informações Médicas e de Saúde
    historico_medico = models.TextField(help_text="Histórico médico detalhado do paciente.", null=True, blank=True)
    alergias = models.TextField(null=True, blank=True)
    medicamentos_em_uso = models.TextField(null=True, blank=True)
    doencas_preexistentes = models.TextField(null=True, blank=True)
    tipo_dependencia = models.CharField(max_length=255, help_text="Ex: álcool, drogas sintéticas.", null=True, blank=True)
    comorbidades_psiquiatricas = models.TextField(null=True, blank=True)

    # Novo campo de análise de risco
    analise_risco = models.FloatField(null=True, blank=True, help_text="Pontuação de risco gerada automaticamente para o paciente.")
    
    # Plano de Saúde e Documentos
    plano_saude = models.CharField(max_length=255, null=True, blank=True)
    numero_cartao_saude = models.CharField(max_length=50, null=True, blank=True)
    documentos_digitalizados = models.JSONField(null=True, blank=True, help_text="Armazena links para documentos digitalizados (RG, CPF, plano de saúde).")

    # Dados de Triagem e Acompanhamento Inicial
    etapa_triagem = models.CharField(max_length=50, choices=[
        ('entrevista_inicial', 'Entrevista Inicial'),
        ('exames', 'Exames Médicos'),
        ('analise_risco', 'Análise de Risco')
    ], default='entrevista_inicial')
    resultado_triagem = models.TextField(null=True, blank=True)
    data_triagem = models.DateField(null=True, blank=True)

    # Informações de Internação
    internacao = models.BooleanField(default=False)
    data_admissao = models.DateField(null=True, blank=True)
    data_alta = models.DateField(null=True, blank=True)
    leito = models.CharField(max_length=50, null=True, blank=True)
    observacoes_internacao = models.TextField(null=True, blank=True)

    # Evolução e Acompanhamento Terapêutico
    evolucao_terapeutica = models.TextField(help_text="Registro detalhado da evolução do paciente durante o tratamento.", null=True, blank=True)
    metas_tratamento = models.TextField(help_text="Metas específicas para o tratamento do paciente.", null=True, blank=True)
    questionarios_periodicos = models.JSONField(null=True, blank=True, help_text="Respostas dos questionários periódicos enviados ao paciente.")
    notas_profissionais = models.TextField(help_text="Notas adicionadas pelos profissionais de saúde.", null=True, blank=True)

    # Relatórios e Assinaturas Digitais
    relatorios_gerados = models.JSONField(null=True, blank=True, help_text="Lista de relatórios gerados automaticamente.")
    assinatura_digital_profissional = models.CharField(max_length=255, null=True, blank=True, help_text="ID da assinatura digital do profissional responsável.")

    # Informações Adicionais
    responsavel_legal = models.CharField(max_length=255, null=True, blank=True)
    consentimento_familiar = models.BooleanField(default=False)
    dados_familiares = models.TextField(null=True, blank=True, help_text="Informações sobre histórico familiar de dependência.")

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"
