from rest_framework import generics
from buildings.models import Building
from .serializers import CreateBuildingSerializer


class CreateBuildingView(generics.CreateAPIView):
    queryset = Building.objects.all()
    serializer_class = CreateBuildingSerializer
