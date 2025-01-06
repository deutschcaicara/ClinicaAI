from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Marketing_smsViewSet

router = DefaultRouter()
router.register(r"marketing_sms", Marketing_smsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
