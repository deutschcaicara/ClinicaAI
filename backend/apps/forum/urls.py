from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForumViewSet

router = DefaultRouter()
router.register(r'forum', ForumViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
