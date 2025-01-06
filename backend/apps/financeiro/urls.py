from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CategoriaFinanceiraViewSet,
    TransacaoViewSet,
    ContaViewSet,
  
    OrcamentoViewSet,
    SimulacaoCenarioViewSet,
    RelatorioFinanceiroViewSet,
    LogAuditoriaViewSet,
)

# Roteador para ViewSets
router = DefaultRouter()
router.register(r"categorias", CategoriaFinanceiraViewSet, basename="categorias")
router.register(r"transacoes", TransacaoViewSet, basename="transacoes")
router.register(r"contas", ContaViewSet, basename="contas")
router.register(r"orcamentos", OrcamentoViewSet, basename="orcamentos")
router.register(r"simulacoes", SimulacaoCenarioViewSet, basename="simulacoes")
router.register(r"relatorios", RelatorioFinanceiroViewSet, basename="relatorios")
router.register(r"logs", LogAuditoriaViewSet, basename="logs")

# URLs adicionais
urlpatterns = router.urls + [
    path(
        "contas/<int:pk>/renegociar/",
        ContaViewSet.as_view({"post": "renegociar"}),
        name="conta-renegociar",
    ),
]
