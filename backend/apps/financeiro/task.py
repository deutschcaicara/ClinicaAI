from celery import shared_task
from datetime import date
from .models import Conta

@shared_task
def enviar_lembretes_vencimento():
    """
    Envia lembretes para contas próximas ao vencimento.
    """
    contas_pendentes = Conta.objects.filter(status="pendente", vencimento__gte=date.today())
    for conta in contas_pendentes:
        # Simulação de envio de notificação (substitua pelo envio real)
        print(f"Notificação enviada para {conta.cliente or conta.fornecedor}: Conta '{conta.descricao}' vence em {conta.vencimento}.")
@shared_task
def enviar_alertas_atraso():
    """
    Envia alertas para contas atrasadas.
    """
    contas_atrasadas = Conta.objects.filter(status="pendente", vencimento__lt=date.today())
    for conta in contas_atrasadas:
        # Simulação de envio de alerta (substitua pelo envio real)
        print(f"Alerta enviado para {conta.cliente or conta.fornecedor}: Conta '{conta.descricao}' está atrasada desde {conta.vencimento}.")
@shared_task
def conciliar_transacoes():
    """
    Concilia automaticamente as transações importadas do banco com as registradas no sistema.
    """
    from .models import TransacaoCartaoCredito, Transacao
    transacoes_banco = TransacaoCartaoCredito.objects.filter(conciliada=False)
    for transacao_banco in transacoes_banco:
        transacao_sistema = Transacao.objects.filter(valor=transacao_banco.valor, data=transacao_banco.data_transacao).first()
        if transacao_sistema:
            transacao_banco.conciliada = True
            transacao_banco.save()
            print(f"Conciliação realizada: Transação '{transacao_sistema.descricao}' conciliada com o banco.")
@shared_task
def gerar_relatorio_financeiro(periodo_inicio, periodo_fim):
    """
    Gera um relatório financeiro para um período específico.
    """
    from .models import Transacao, RelatorioFinanceiro
    receitas = Transacao.objects.filter(tipo="receita", data__range=[periodo_inicio, periodo_fim]).aggregate(models.Sum("valor"))["valor__sum"] or 0
    despesas = Transacao.objects.filter(tipo="despesa", data__range=[periodo_inicio, periodo_fim]).aggregate(models.Sum("valor"))["valor__sum"] or 0
    saldo = receitas - despesas

    relatorio = RelatorioFinanceiro.objects.create(
        tipo="Relatório Financeiro",
        descricao=f"Relatório financeiro de {periodo_inicio} a {periodo_fim}.",
        periodo_inicio=periodo_inicio,
        periodo_fim=periodo_fim,
        conteudo={
            "receitas": receitas,
            "despesas": despesas,
            "saldo": saldo,
        },
    )
    print(f"Relatório financeiro gerado: {relatorio.id}")
