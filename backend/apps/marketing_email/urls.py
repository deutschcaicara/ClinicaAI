from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Marketing_emailViewSet

router = DefaultRouter()
router.register(r"marketing_email", Marketing_emailViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
