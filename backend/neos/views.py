from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CloseApproach, NearEarthObject
from .serializers import CloseApproachSerializer, NearEarthObjectSerializer

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})

class NearEarthObjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NearEarthObject.objects.all()
    serializer_class = NearEarthObjectSerializer


class CloseApproachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CloseApproach.objects.select_related("near_earth_object").all()
    serializer_class = CloseApproachSerializer