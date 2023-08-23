"""Views file"""

from rest_framework import viewsets

from api.serializers import (
    ChampionSerializer,
    ChampionCreateUpdateSerializer,
    RoleSerializer,
    AbilitySerializer,
    AbilityCreateUpdateSerializer
)

from core.models import (
    Champion,
    Role,
    Ability
)

# Create your views here.


class ChampionViewSet(viewsets.ModelViewSet):
    """View for manage Champions API"""
    serializer_class = ChampionSerializer
    queryset = Champion.objects.all()

    def get_serializer_class(self):
        create_update_actions = ['create', 'update', 'partial_update']
        if self.action in create_update_actions:
            return ChampionCreateUpdateSerializer
        return ChampionSerializer


class RoleViewSet(viewsets.ModelViewSet):
    """View for manage Roles API"""
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class AbilityViewSet(viewsets.ModelViewSet):
    """View for manage Abilities API"""
    serializer_class = AbilitySerializer
    queryset = Ability.objects.all()

    def get_serializer_class(self):
        create_update_actions = ['create', 'update', 'partial_update']
        if self.action in create_update_actions:
            return AbilityCreateUpdateSerializer
        return AbilitySerializer
