from django.db import models
from apps.pacientes.models import Paciente
from apps.profissionais.models import Profissional
from apps.compras.models import Fornecedor
from apps.clinica_core.models import Documento
from datetime import timedelta


# Categorias de receitas/despesas
class CategoriaFinanceira(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    subcategoria = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Subcategoria"
    )
    ativa = models.BooleanField(default=True, verbose_name="Categoria Ativa")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
criado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_criador")
atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
atualizado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_atualizador")

class Meta:
        verbose_name = "Categoria Financeira"
        verbose_name_plural = "Categorias Financeiras"
        ordering = ["nome"]

def __str__(self):
        return self.nome


# Controle de transações (receitas e despesas)
class Transacao(models.Model):
    TIPO_CHOICES = [
        ("receita", "Receita"),
        ("despesa", "Despesa"),
    ]

    FORMA_PAGAMENTO_CHOICES = [
        ("dinheiro", "Dinheiro"),
        ("cartao", "Cartão"),
        ("pix", "PIX"),
        ("transferencia", "Transferência Bancária"),
        ("plano_saude", "Plano de Saúde"),
    ]

    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name="Tipo")
    forma_pagamento = models.CharField(
        max_length=50, choices=FORMA_PAGAMENTO_CHOICES, verbose_name="Forma de Pagamento", blank=True, null=True
    )
    categoria = models.ForeignKey(
        CategoriaFinanceira, on_delete=models.SET_NULL, null=True, verbose_name="Categoria"
    )
    origem_rh = models.ForeignKey(
        "recursos_humanos.PagamentoFuncionario", on_delete=models.SET_NULL, null=True, verbose_name="Pagamento de Funcionário"
    )
    tags = models.CharField(max_length=255, blank=True, verbose_name="Tags")
    data = models.DateField(auto_now_add=True, verbose_name="Data da Transação")
    paciente = models.ForeignKey(
        Paciente, on_delete=models.SET_NULL, null=True, blank=True, related_name="transacoes"
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name="despesas"
    )
    centro_custo = models.CharField(max_length=100, blank=True, verbose_name="Centro de Custo")
    anexos = models.FileField(upload_to="financeiro/anexos/", blank=True, null=True, verbose_name="Anexos")
    status = models.CharField(
        max_length=20,
        choices=[
            ("pendente", "Pendente"),
            ("pago", "Pago"),
            ("atrasado", "Atrasado"),
        ],
        default="pendente",
    )
    categoria_sugerida = models.ForeignKey(
        CategoriaFinanceira,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transacoes_sugeridas",
        verbose_name="Categoria Sugerida",
    )
    @classmethod
    def buscar_por_tag(cls, tag):
        """
        Busca transações que contenham a tag fornecida.
        """
        return cls.objects.filter(tags__icontains=tag)

    @classmethod
    def soma_por_categoria(cls, categoria_id):
        """
        Calcula a soma dos valores das transações de uma categoria específica.
        """
        return cls.objects.filter(categoria_id=categoria_id).aggregate(models.Sum("valor"))["valor__sum"]


criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
criado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_criador")
atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
atualizado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_atualizador")

class Meta:
        ordering = ["-data"]
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

def __str__(self):
        return f"{self.descricao} - {self.valor}"



class Conta(models.Model):
    TIPO_CHOICES = [
        ("pagar", "A Pagar"),
        ("receber", "A Receber"),
    ]

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("atrasado", "Atrasado"),
        ("renegociado", "Renegociado"),
        ("cancelado", "Cancelado"),
    ]

    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name="Tipo")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    vencimento = models.DateField(verbose_name="Data de Vencimento")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pendente", verbose_name="Status"
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fornecedor"
    )
    origem_pedido = models.ForeignKey(
        "compras.PedidoFornecedor", on_delete=models.SET_NULL, null=True, verbose_name="Pedido do Fornecedor"
    )
    cliente = models.ForeignKey(
        Paciente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente"
    )
    categoria = models.ForeignKey(
        CategoriaFinanceira, on_delete=models.SET_NULL, null=True, verbose_name="Categoria"
    )
    parcelada = models.BooleanField(default=False, verbose_name="É Parcelada?")
    numero_parcelas = models.PositiveIntegerField(default=1, verbose_name="Número de Parcelas")
    parcela_atual = models.PositiveIntegerField(default=1, verbose_name="Parcela Atual")
    juros = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Juros (%)")
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Multa (Valor)")
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Desconto")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    documentos = models.ManyToManyField(Documento, blank=True, verbose_name="Documentos")
    identificador_bancario = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID Bancário")
    referencia_externa = models.CharField(max_length=255, blank=True, null=True, verbose_name="Referência Externa")
    impacto_fluxo_caixa = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Impacto no Fluxo de Caixa"
    )

    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    criado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_criador")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    atualizado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, related_name="%(class)s_atualizador")

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        ordering = ["-vencimento"]
    def calcular_impacto_fluxo_caixa(self):
        """
        Calcula o impacto da conta no fluxo de caixa projetado.
        """
        if self.status == "pendente":
            self.impacto_fluxo_caixa = self.valor
        elif self.status == "pago":
            self.impacto_fluxo_caixa = 0
        self.save()
    def __str__(self):
        return f"{self.descricao} - {self.valor} ({self.status})"

    def calcular_valor_atualizado(self):
        """
        Calcula o valor atualizado da conta, considerando juros e multas em caso de atraso.
        """
        from datetime import date
        if self.status == "atrasado" and self.vencimento < date.today():
            dias_atraso = (date.today() - self.vencimento).days
            juros_calculado = self.valor * (self.juros / 100) * dias_atraso
            return self.valor + juros_calculado + self.multa
        return self.valor

    def aplicar_desconto(self):
        """
        Aplica o desconto se a conta for paga antes do vencimento.
        """
        if self.status == "pendente":
            self.valor -= self.desconto
            self.desconto = 0
            self.save()

    def gerar_parcelas(self):
        """
        Gera parcelas automáticas para contas parceladas.
        """
        if self.parcelada and self.numero_parcelas > 1:
            valor_parcela = self.valor / self.numero_parcelas
            for parcela in range(2, self.numero_parcelas + 1):
                Conta.objects.create(
                    descricao=f"{self.descricao} - Parcela {parcela}",
                    tipo=self.tipo,
                    valor=valor_parcela,
                    vencimento=self.vencimento + timedelta(days=30 * (parcela - 1)),
                    status="pendente",
                    fornecedor=self.fornecedor,
                    cliente=self.cliente,
                    parcelada=True,
                    numero_parcelas=self.numero_parcelas,
                    parcela_atual=parcela,
                )



# Controle de orçamentos
class Orcamento(models.Model):
    centro_custo = models.CharField(max_length=100, verbose_name="Centro de Custo")
    periodo_inicio = models.DateField(verbose_name="Início do Período")
    periodo_fim = models.DateField(verbose_name="Fim do Período")
    valor_planejado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Planejado")
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor Gasto")

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        ordering = ["-periodo_inicio"]

    def __str__(self):
        return f"Orçamento {self.centro_custo} ({self.periodo_inicio} - {self.periodo_fim})"

    def calcular_percentual_gasto(self):
        """
        Retorna o percentual do orçamento já utilizado.
        """
        if self.valor_planejado > 0:
            return (self.valor_gasto / self.valor_planejado) * 100
        return 0

    def alerta_sobre_orcamento(self):
        """
        Verifica se o gasto ultrapassou o orçamento planejado.
        """
        return self.valor_gasto > self.valor_planejado


# Relatórios financeiros
class Relatorio(models.Model):
    tipo = models.CharField(max_length=50, verbose_name="Tipo do Relatório")
    periodo_inicio = models.DateField(verbose_name="Início do Período")
    periodo_fim = models.DateField(verbose_name="Fim do Período")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    conteudo = models.JSONField(verbose_name="Conteúdo do Relatório")
    analise_automatica = models.JSONField(blank=True, null=True, verbose_name="Análise Gerada por IA")
    insights = models.TextField(blank=True, null=True, verbose_name="Insights Automáticos")

    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"

    def __str__(self):
        return f"Relatório {self.tipo} ({self.periodo_inicio} - {self.periodo_fim})"
class Renegociacao(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name="renegociacoes")
    data_renegociacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Renegociação")
    novo_valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Novo Valor")
    nova_data_vencimento = models.DateField(verbose_name="Nova Data de Vencimento")
    condicoes = models.TextField(verbose_name="Condições Negociadas", blank=True, null=True)

    class Meta:
        verbose_name = "Renegociação"
        verbose_name_plural = "Renegociações"
        ordering = ["-data_renegociacao"]

    def __str__(self):
        return f"Renegociação - {self.conta.descricao} em {self.data_renegociacao}"
class SimulacaoCenario(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Cenário")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="simulacoes")
    impacto_receitas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Impacto nas Receitas", default=0)
    impacto_despesas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Impacto nas Despesas", default=0)
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Simulação de Cenário"
        verbose_name_plural = "Simulações de Cenários"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Simulação {self.nome} ({self.orcamento.centro_custo})"

    def calcular_saldo_simulado(self):
        """
        Calcula o saldo projetado considerando o impacto de receitas e despesas.
        """
        saldo_atual = self.orcamento.valor_planejado - self.orcamento.valor_gasto
        return saldo_atual + self.impacto_receitas - self.impacto_despesas
class AlertaOrcamento(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="alertas")
    descricao = models.CharField(max_length=255, verbose_name="Descrição do Alerta")
    limite_percentual = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Limite Percentual", default=100
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Alerta de Orçamento"
        verbose_name_plural = "Alertas de Orçamento"

    def __str__(self):
        return f"Alerta ({self.orcamento.centro_custo}) - {self.descricao}"
class AnaliseSensibilidade(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="analises")
    variavel = models.CharField(max_length=100, verbose_name="Variável Analisada")
    variacao_percentual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Variação (%)")
    impacto_estimado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Impacto Estimado")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Análise de Sensibilidade"
        verbose_name_plural = "Análises de Sensibilidade"

    def __str__(self):
        return f"Análise ({self.orcamento.centro_custo}) - {self.variavel}"
class RelatorioFinanceiro(models.Model):
    tipo = models.CharField(max_length=50, verbose_name="Tipo do Relatório")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    periodo_inicio = models.DateField(verbose_name="Início do Período")
    periodo_fim = models.DateField(verbose_name="Fim do Período")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    conteudo = models.JSONField(verbose_name="Conteúdo do Relatório")
    exportado = models.BooleanField(default=False, verbose_name="Exportado?")
    formato_exportado = models.CharField(
        max_length=10, choices=[("excel", "Excel"), ("pdf", "PDF"), ("csv", "CSV"), ("html", "HTML")], blank=True, null=True
    )

    class Meta:
        verbose_name = "Relatório Financeiro"
        verbose_name_plural = "Relatórios Financeiros"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Relatório {self.tipo} ({self.periodo_inicio} - {self.periodo_fim})"
class LogAuditoria(models.Model):
    usuario = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, verbose_name="Usuário")
    acao = models.CharField(max_length=255, verbose_name="Ação Realizada")
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")
    detalhes = models.JSONField(verbose_name="Detalhes da Ação", blank=True, null=True)
    ip_origem = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP de Origem")

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ["-data_hora"]

    def __str__(self):
        return f"{self.usuario} - {self.acao} em {self.data_hora}"
class RelatorioCustomizado(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Relatório")
    campos = models.JSONField(verbose_name="Campos Selecionados")
    filtros = models.JSONField(blank=True, null=True, verbose_name="Filtros Aplicados")
    criado_por = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, verbose_name="Criado Por")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Relatório Customizado"
        verbose_name_plural = "Relatórios Customizados"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Relatório Customizado - {self.nome}"
class GatewayPagamento(models.Model):
    TIPO_GATEWAY_CHOICES = [
        ("pagseguro", "PagSeguro"),
        ("mercado_pago", "Mercado Pago"),
        ("paypal", "PayPal"),
        ("outros", "Outros"),
    ]

    transacao = models.OneToOneField(
        "Transacao", on_delete=models.CASCADE, related_name="gateway", verbose_name="Transação"
    )
    id_transacao_gateway = models.CharField(max_length=255, verbose_name="ID da Transação no Gateway")
    tipo_gateway = models.CharField(max_length=50, choices=TIPO_GATEWAY_CHOICES, verbose_name="Tipo de Gateway")
    status_pagamento = models.CharField(
        max_length=50,
        choices=[
            ("pendente", "Pendente"),
            ("pago", "Pago"),
            ("cancelado", "Cancelado"),
            ("falha", "Falha"),
        ],
        verbose_name="Status do Pagamento",
    )
    data_pagamento = models.DateTimeField(blank=True, null=True, verbose_name="Data do Pagamento")

    class Meta:
        verbose_name = "Gateway de Pagamento"
        verbose_name_plural = "Gateways de Pagamento"
        ordering = ["-data_pagamento"]

    def __str__(self):
        return f"{self.tipo_gateway} - {self.id_transacao_gateway} ({self.status_pagamento})"
class TransacaoCartaoCredito(models.Model):
    operadora = models.CharField(max_length=100, verbose_name="Operadora")
    id_transacao = models.CharField(max_length=255, verbose_name="ID da Transação na Operadora")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    data_transacao = models.DateTimeField(verbose_name="Data da Transação")
    conciliada = models.BooleanField(default=False, verbose_name="Conciliada?")

    class Meta:
        verbose_name = "Transação de Cartão de Crédito"
        verbose_name_plural = "Transações de Cartão de Crédito"
        ordering = ["-data_transacao"]

    def __str__(self):
        return f"{self.operadora} - {self.id_transacao} ({'Conciliada' if self.conciliada else 'Não Conciliada'})"

    
class RiscoCredito(models.Model):
    cliente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Cliente")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score de Risco")
    data_calculo = models.DateTimeField(auto_now_add=True, verbose_name="Data do Cálculo")

    class Meta:
        verbose_name = "Risco de Crédito"
        verbose_name_plural = "Riscos de Crédito"
        ordering = ["-data_calculo"]

    def __str__(self):
        return f"{self.cliente} - Score: {self.score}"
class Cobranca(models.Model):
    conta = models.ForeignKey("Conta", on_delete=models.CASCADE, related_name="cobrancas")
    data_acao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Ação")
    tipo_acao = models.CharField(
        max_length=50,
        choices=[
            ("lembrete", "Lembrete"),
            ("contato", "Contato Direto"),
            ("negociacao", "Negociação"),
        ],
        verbose_name="Tipo de Ação",
    )
    detalhes = models.TextField(blank=True, null=True, verbose_name="Detalhes da Cobrança")
    responsavel = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, verbose_name="Responsável")

    class Meta:
        verbose_name = "Cobrança"
        verbose_name_plural = "Cobranças"
        ordering = ["-data_acao"]

    def __str__(self):
        return f"{self.tipo_acao} - {self.conta.descricao} ({self.data_acao})"
class Contrato(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name="Fornecedor")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_termino = models.DateField(blank=True, null=True, verbose_name="Data de Término")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total")
    clausulas = models.TextField(verbose_name="Cláusulas do Contrato", blank=True, null=True)
    documentos = models.ManyToManyField(Documento, blank=True, verbose_name="Documentos Anexados")

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ["-data_inicio"]

    def __str__(self):
        return f"Contrato com {self.fornecedor} ({self.data_inicio} - {self.data_termino})"










