from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfissionaiViewSet

router = DefaultRouter()
router.register(r'profissionaiss', ProfissionaiViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
