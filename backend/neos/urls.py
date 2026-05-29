from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CloseApproachViewSet, NearEarthObjectViewSet

router = DefaultRouter()
router.register("neos", NearEarthObjectViewSet, basename="neo")
router.register("approaches", CloseApproachViewSet, basename="approach")

urlpatterns = [
    path("", include(router.urls)),
]
