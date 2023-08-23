"""Lol-API serializares"""

from rest_framework import serializers

from core.models import Role, Champion, Ability


class RoleSerializer(serializers.ModelSerializer):
    """Serilizer for roles"""
    class Meta:
        model = Role
        fields = ['id', 'name']
        read_only = ['id']


class AbilitySerializer(serializers.ModelSerializer):
    """Serializer for the Abilities"""
    class Meta:
        model = Ability
        fields = ['id', 'name', 'owner']
        read_only = ['id']


class ChampionSerializer(serializers.ModelSerializer):
    """Serializer for champions"""
    # Nested serializer
    abilities = AbilitySerializer(many=True, source='ability_set')
    # Custom role field, now respond the role's name
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Champion
        fields = ['id', 'name', 'roles', 'abilities']
        read_only = ['id', 'roles']

    def get_roles(self, Champion):
        """Custom method that returns a list of the role names"""
        roles = Champion.role.all()
        roles_names = [role.name for role in roles]
        return roles_names
