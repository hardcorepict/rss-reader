from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChannelViewSet

router = DefaultRouter()
router.register("channels", ChannelViewSet, basename="channels")

urlpatterns = [
    path("", include(router.urls)),
]
