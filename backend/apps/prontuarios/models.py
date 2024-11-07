# Módulo Prontuários - Criação do Modelo (models.py)

from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings

class Prontuario(models.Model):
    # Identificador Único Global
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # Dados Relacionados ao Paciente
    paciente = models.OneToOneField('pacientes.Paciente', on_delete=models.CASCADE, related_name='prontuario')

    # Evoluções Clínicas e Atendimentos
    data_atendimento = models.DateTimeField(_("Data do Atendimento"))
    profissional_responsavel = models.ForeignKey('profissionais.Profissional', on_delete=models.SET_NULL, null=True, related_name='atendimentos_realizados')
    queixa_principal = models.TextField(_("Queixa Principal"), blank=True)
    historico_doenca_atual = models.TextField(_("Histórico da Doença Atual"), blank=True)
    antecedentes_pessoais = models.TextField(_("Antecedentes Pessoais"), blank=True)
    exame_fisico_cabeca_pescoco = models.TextField(_("Exame Físico - Cabeça e Pescoço"), blank=True)
    exame_fisico_torax = models.TextField(_("Exame Físico - Tórax"), blank=True)
    exame_fisico_abdomen = models.TextField(_("Exame Físico - Abdômen"), blank=True)
    exame_fisico_membros = models.TextField(_("Exame Físico - Membros Superiores e Inferiores"), blank=True)
    hipotese_diagnostica = models.TextField(_("Hipótese Diagnóstica"), blank=True)
    conduta = models.TextField(_("Conduta/Plano"), blank=True)
    prescricao = models.TextField(_("Prescrição Médica"), blank=True)
    tratamentos_previos = models.TextField(_("Tratamentos Prévio(s)"), blank=True)

    # Diagnósticos
    diagnostico_final = models.CharField(_("Diagnóstico Final"), max_length=255, blank=True)
    cid_10 = models.CharField(_("CID-10"), max_length=10, blank=True)

    # Anotações de Outros Profissionais
    anotacoes_profissionais = models.TextField(_("Anotações de Outros Profissionais"), blank=True)

    # Referências e Encaminhamentos
    encaminhamentos = models.TextField(_("Encaminhamentos"), blank=True)
    referencias_especialidades = models.TextField(_("Referências para Especialidades"), blank=True)

    # Consentimento e Termos
    consentimento_informado = models.BooleanField(_("Consentimento Informado Assinado"), default=False)

    # Histórico Familiar
    historico_familiar = models.TextField(_("Histórico Familiar"), blank=True)
    risco_genetico = models.TextField(_("Risco Genético Identificado"), blank=True)

    # Dados Psicológicos e Sociais
    dados_psicossociais = models.TextField(_("Dados Psicológicos e Sociais"), blank=True)
    estado_emocional = models.TextField(_("Estado Emocional"), blank=True)
    transtornos_identificados = models.TextField(_("Transtornos Identificados"), blank=True)
    medicacoes_psiquiatricas = models.TextField(_("Medicações Psiquiátricas"), blank=True)

    # Histórico de Hábitos de Vida
    tabagismo = models.BooleanField(_("Tabagismo"), default=False)
    etilismo = models.BooleanField(_("Etilismo"), default=False)
    uso_drogas = models.BooleanField(_("Uso de Drogas"), default=False)
    atividade_fisica = models.CharField(_("Atividade Física"), max_length=255, blank=True)
    alimentacao = models.CharField(_("Alimentação"), max_length=255, blank=True)
    qualidade_sono = models.CharField(_("Qualidade do Sono"), max_length=255, blank=True)
    ocupacao = models.CharField(_("Ocupação"), max_length=255, blank=True)
    nivel_estresse = models.CharField(_("Nível de Estresse"), max_length=255, blank=True)
    medicacoes_nao_prescritas = models.TextField(_("Medicações Não Prescritas"), blank=True)

    # Histórico de Cirurgias e Internações
    historico_cirurgias = models.TextField(_("Histórico de Cirurgias"), blank=True)
    historico_internacoes = models.TextField(_("Histórico de Internações"), blank=True)

    # Histórico de Imunizações
    imunizacoes = models.TextField(_("Histórico de Imunizações"), blank=True)

    # Estratificação de Risco
    estratificacao_risco = models.CharField(_("Estratificação de Risco"), max_length=255, blank=True)
    risco_quedas = models.CharField(_("Risco de Quedas"), max_length=255, blank=True)

    # Motivo do Atendimento
    motivo_atendimento = models.CharField(_("Motivo do Atendimento"), max_length=255, blank=True)

    # Acompanhamento de Doenças Crônicas
    diabetes_hemoglobina_glicada = models.DecimalField(_("Hemoglobina Glicada (%)"), max_digits=4, decimal_places=2, blank=True, null=True)
    funcao_renal_taxa_filtracao = models.DecimalField(_("Taxa de Filtração Glomerular (mL/min)"), max_digits=5, decimal_places=2, blank=True, null=True)

    # Avaliação Nutricional
    imc = models.DecimalField(_("Índice de Massa Corporal (IMC)"), max_digits=4, decimal_places=1, blank=True, null=True)
    percentual_gordura_corporal = models.DecimalField(_("Percentual de Gordura Corporal (%)"), max_digits=4, decimal_places=1, blank=True, null=True)
    dieta_recomendada = models.TextField(_("Dieta Recomendada"), blank=True)

    # Planos de Saúde e Seguros
    plano_saude = models.CharField(_("Plano de Saúde"), max_length=255, blank=True)
    numero_plano_saude = models.CharField(_("Número do Plano de Saúde"), max_length=255, blank=True)

    # Auditoria
    created_at = models.DateTimeField(_("Data de Criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Última Atualização"), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='prontuarios_criados')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='prontuarios_atualizados')

    class Meta:
        verbose_name = _("Prontuário")
        verbose_name_plural = _("Prontuários")

    def __str__(self):
        return f"Prontuário do paciente: {self.paciente.nome_completo}"

class HistoricoMedicamentos(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='historico_medicamentos')
    medicamento = models.CharField(_("Medicamento"), max_length=255)
    dosagem = models.CharField(_("Dosagem"), max_length=255)
    frequencia = models.CharField(_("Frequência"), max_length=255)
    duracao = models.CharField(_("Duração"), max_length=255)
    observacoes = models.TextField(_("Observações"), blank=True)
    prescrito_por = models.ForeignKey('profissionais.Profissional', on_delete=models.SET_NULL, null=True)
    data_prescricao = models.DateTimeField(_("Data da Prescrição"), auto_now_add=True)

    class Meta:
        verbose_name = _("Histórico de Medicamento")
        verbose_name_plural = _("Histórico de Medicamentos")

    def __str__(self):
        return f"Medicamento: {self.medicamento} - Paciente: {self.prontuario.paciente.nome_completo}"

class EvolucaoClinica(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='evolucoes_clinicas')
    data_evolucao = models.DateTimeField(_("Data da Evolução"), auto_now_add=True)
    profissional_responsavel = models.ForeignKey('profissionais.Profissional', on_delete=models.SET_NULL, null=True)
    descricao = models.TextField(_("Descrição da Evolução"))

    class Meta:
        verbose_name = _("Evolução Clínica")
        verbose_name_plural = _("Evoluções Clínicas")

    def __str__(self):
        return f"Evolução em {self.data_evolucao} - Paciente: {self.prontuario.paciente.nome_completo}"

class DadosVitais(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='dados_vitais')
    data_registro = models.DateTimeField(_("Data do Registro"), auto_now_add=True)
    pressao_arterial = models.CharField(_("Pressão Arterial"), max_length=50, blank=True)
    frequencia_cardiaca = models.CharField(_("Frequência Cardíaca"), max_length=50, blank=True)
    temperatura = models.DecimalField(_("Temperatura Corporal (°C)"), max_digits=4, decimal_places=1, blank=True, null=True)
    saturacao_oxigenio = models.CharField(_("Saturação de Oxigênio (%)"), max_length=50, blank=True)
    peso = models.DecimalField(_("Peso (kg)"), max_digits=5, decimal_places=2, blank=True, null=True)
    altura = models.DecimalField(_("Altura (m)"), max_digits=4, decimal_places=2, blank=True, null=True)
    glicemia = models.DecimalField(_("Glicemia (mg/dL)"), max_digits=5, decimal_places=2, blank=True, null=True)
    colesterol_total = models.DecimalField(_("Colesterol Total (mg/dL)"), max_digits=5, decimal_places=2, blank=True, null=True)
    triglicerides = models.DecimalField(_("Triglicérides (mg/dL)"), max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _("Dados Vitais")
        verbose_name_plural = _("Dados Vitais")

    def __str__(self):
        return f"Dados Vitais em {self.data_registro} - Paciente: {self.prontuario.paciente.nome_completo}"

class HistoricoAcessosProntuario(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='historico_acessos')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_acesso = models.DateTimeField(_("Data do Acesso"), auto_now_add=True)
    tipo_acesso = models.CharField(_("Tipo de Acesso"), max_length=50, choices=[('visualizacao', 'Visualização'), ('alteracao', 'Alteração')])

    class Meta:
        verbose_name = _("Histórico de Acesso ao Prontuário")
        verbose_name_plural = _("Histórico de Acessos ao Prontuário")

    def __str__(self):
        return f"Acesso em {self.data_acesso} - Paciente: {self.prontuario.paciente.nome_completo} por {self.usuario}"

class ExameComplementar(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='exames_complementares')
    tipo_exame = models.CharField(_("Tipo de Exame"), max_length=255)
    data_solicitacao = models.DateTimeField(_("Data da Solicitação"), auto_now_add=True)
    data_resultado = models.DateTimeField(_("Data do Resultado"), null=True, blank=True)
    resultado = models.TextField(_("Resultado do Exame"), blank=True)
    profissional_responsavel = models.ForeignKey('profissionais.Profissional', on_delete=models.SET_NULL, null=True, related_name='exames_solicitados')
    imagem_associada = models.ImageField(_("Imagem Associada"), upload_to='exames/imagens/', blank=True, null=True)

    class Meta:
        verbose_name = _("Exame Complementar")
        verbose_name_plural = _("Exames Complementares")

    def __str__(self):
        return f"Exame: {self.tipo_exame} - Paciente: {self.prontuario.paciente.nome_completo}"

class ProcedimentoRealizado(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='procedimentos_realizados')
    tipo_procedimento = models.CharField(_("Tipo de Procedimento"), max_length=255)
    data_procedimento = models.DateTimeField(_("Data do Procedimento"), auto_now_add=True)
    profissional_responsavel = models.ForeignKey('profissionais.Profissional', on_delete=models.SET_NULL, null=True, related_name='procedimentos_realizados')
    observacoes = models.TextField(_("Observações"), blank=True)
    consentimento_associado = models.ForeignKey('assinaturas.Assinatura', on_delete=models.SET_NULL, null=True, blank=True, related_name='procedimentos_consentidos')

    class Meta:
        verbose_name = _("Procedimento Realizado")
        verbose_name_plural = _("Procedimentos Realizados")
