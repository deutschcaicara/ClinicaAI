from rest_framework.routers import DefaultRouter
from .views import LogSistemaViewSet, DocumentoViewSet

router = DefaultRouter()
router.register(r"logs", LogSistemaViewSet, basename="log-sistema")
router.register(r"documentos", DocumentoViewSet, basename="documento")

urlpatterns = router.urls
