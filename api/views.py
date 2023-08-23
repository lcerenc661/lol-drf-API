"""Views file"""

from rest_framework import viewsets

from api.serializers import ChampionSerializer
from core.models import Champion

# Create your views here.


class ChampionViewSet(viewsets.ModelViewSet):
    """View for manage Champions API"""
    serializer_class = ChampionSerializer
    queryset = Champion.objects.all()
