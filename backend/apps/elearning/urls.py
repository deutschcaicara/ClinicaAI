from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ElearningViewSet

router = DefaultRouter()
router.register(r'elearning', ElearningViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
