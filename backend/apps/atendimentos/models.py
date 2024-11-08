from django.db import models
from django.utils import timezone
from apps.pacientes.models import Paciente
from apps.profissionais.models import Profissional
from apps.agendamentos.models import Agendamento
from apps.documentos.models import DocumentosModel
from apps.financeiro.models import Transacao
from apps.assinaturas.models import Assinatura
from apps.prontuarios.models import ProcedimentoRealizado

# Ajuste o caminho conforme a localização do modelo
from apps.iot.models import DispositivoIoT


class Atendimento(models.Model):
    STATUS_CHOICES = [
        ("Pendente", "Pendente"),
        ("Em Andamento", "Em Andamento"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
        ("Aguardando Documentação", "Aguardando Documentação"),
        ("Aguardando Pagamento", "Aguardando Pagamento"),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="atendimentos"
    )
    profissional = models.ForeignKey(
        Profissional, on_delete=models.CASCADE, related_name="atendimentos"
    )
    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atendimento",
    )
    procedimentos = models.ManyToManyField(
        ProcedimentoRealizado, related_name="atendimentos", blank=True
    )
    dispositivos_iot = models.ManyToManyField(
        DispositivoIoT, related_name="atendimentos", blank=True
    )
    # seguro_saude = models.ForeignKey(SeguroSaude, on_delete=models.SET_NULL, null=True, blank=True, related_name='atendimentos')
    data_atendimento = models.DateField(default=timezone.now)
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pendente")
    diagnostico = models.TextField(null=True, blank=True)
    prescricao = models.TextField(null=True, blank=True)
    tratamento = models.TextField(null=True, blank=True)
    assinatura_profissional = models.ForeignKey(
        Assinatura,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assinaturas_profissionais",
    )
    autorizacao_paciente = models.ForeignKey(
        Assinatura,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="autorizacoes_pacientes",
    )
    feedback_paciente = models.TextField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transacao_financeira = models.OneToOneField(
        Transacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="atendimento",
    )
    recomendacoes_ia = models.TextField(null=True, blank=True)
    recomendacoes_automaticas = models.TextField(null=True, blank=True)
    avaliacao_risco = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    consentimento_paciente = models.BooleanField(default=False)
    documentacao_completa = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"
        ordering = ["-data_atendimento", "-horario_inicio"]

    def __str__(self):
        return f"Atendimento de {self.paciente.nome_completo} com {self.profissional.nome_completo} em {self.data_atendimento}"

    def save(self, *args, **kwargs):
        # Lógica adicional para integração com IoT, IA e outros serviços
        if self.status == "Concluído" and not self.transacao_financeira:
            # Cria uma transação financeira se o atendimento for concluído
            self.transacao_financeira = Transacao.objects.create(
                paciente=self.paciente,
                valor=self.valor,
                descricao=f"Pagamento pelo atendimento em {self.data_atendimento}",
                status="Pendente",
            )

        # Integração com IA e Machine Learning para análise do atendimento
        # Exemplo: Enviar dados para serviço de IA para sugerir tratamentos ou
        # analisar feedback

        super().save(*args, **kwargs)

    def finalizar_atendimento(self):
        # Método para finalizar o atendimento e garantir todas as validações
        # necessárias
        if self.status == "Concluído":
            if not self.assinatura_profissional or not self.autorizacao_paciente:
                raise ValueError(
                    "Assinatura do profissional e autorização do paciente são obrigatórias para concluir o atendimento."
                )
            if not self.diagnostico or not self.prescricao:
                raise ValueError(
                    "Diagnóstico e prescrição são obrigatórios para concluir o atendimento."
                )

        # Atualiza o status do agendamento associado
        if self.agendamento:
            self.agendamento.status = "Concluído"
            self.agendamento.save()

        # Enviar notificações para o paciente e profissional

        self.save()


class AuditoriaAtendimento(models.Model):
    atendimento = models.ForeignKey(
        Atendimento, on_delete=models.CASCADE, related_name="auditorias"
    )
    usuario = models.CharField(max_length=255)
    alteracoes = models.TextField()
    data_alteracao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auditoria de Atendimento"
        verbose_name_plural = "Auditorias de Atendimentos"
        ordering = ["-data_alteracao"]

    def __str__(self):
        return f"Auditoria do Atendimento {self.atendimento.id} por {self.usuario} em {self.data_alteracao}"
