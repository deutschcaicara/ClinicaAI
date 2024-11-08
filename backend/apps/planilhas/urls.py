from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanilhasViewSet

router = DefaultRouter()
router.register(r"planilhas", PlanilhasViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
