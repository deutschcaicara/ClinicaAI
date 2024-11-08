from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrmViewSet

router = DefaultRouter()
router.register(r"crm", CrmViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
