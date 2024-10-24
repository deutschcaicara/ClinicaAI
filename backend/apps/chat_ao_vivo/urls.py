from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Chat_ao_vivoViewSet

router = DefaultRouter()
router.register(r'chat_ao_vivo', Chat_ao_vivoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
