"""Lol-API serializares"""

from rest_framework import serializers

from core.models import Role, Champion, Ability

from typing import List


class RoleSerializer(serializers.ModelSerializer):
    """Serilizer for roles"""
    class Meta:
        model = Role
        fields = ['id', 'name']
        read_only = ['id']


class AbilitySerializer(serializers.ModelSerializer):
    """Serializer for the Abilities"""
    champion = serializers.SerializerMethodField()
    ability_id = serializers.PrimaryKeyRelatedField(
        source='id', read_only=True)
    champion_id = serializers.PrimaryKeyRelatedField(
        source='owner', read_only=True)

    class Meta:
        model = Ability
        fields = ['ability_id', 'name', 'champion', 'champion_id']
        read_only = ['id']

    def get_champion(self, Ability):
        return Ability.owner.name


class AbilityCreateUpdateSerializer(AbilitySerializer):
    champion = serializers.CharField(write_only=True)

    def create(self, validated_data):
        owner_name = validated_data.pop('champion', '')
        owner = Champion.objects.filter(name=owner_name).first()
        if owner is not None:
            ability = Ability.objects.create(owner=owner, **validated_data)
            return ability

    def update(self, instance, validated_data):
        owner_name = validated_data.pop('champion', None)

        if owner_name is not None:
            owner = Champion.objects.filter(name=owner_name).first()
            setattr(instance, "owner", owner)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class SimpleAbilitySerializer(AbilitySerializer):
    """Simplified ability serializer for nested serializers"""
    class Meta(AbilitySerializer.Meta):
        fields = ['name']


class ChampionSerializer(serializers.ModelSerializer):
    """Serializer for champions"""
    # Nested serializer
    abilities = SimpleAbilitySerializer(
        many=True, source='ability_set', read_only=True)
    # Custom role field, now respond the role's name
    roles = serializers.SerializerMethodField()

    class Meta:
        model = Champion
        fields = ['id', 'name', 'roles', 'abilities']
        read_only_fields = ['id', 'abilities']

    def get_roles(self, Champion) -> List[str]:
        """Custom method that returns a list of the role names"""
        roles = Champion.role.all()
        roles_names = [role.name for role in roles]
        return roles_names


class ChampionCreateUpdateSerializer(ChampionSerializer):
    roles = serializers.ListField(write_only=True)

    def _handle_roles(self, champion, roles):
        """Handle getting roles as needed"""
        for role in roles:
            role_obj = Role.objects.filter(name=role).first()
            if role_obj is not None:
                print(f"Role name: {role}, Role object: {role_obj}")
                champion.role.add(role_obj)
            else:
                print(f'{role} is not a valid role')

    def create(self, validated_data):
        """Create a champion"""
        roles = validated_data.pop('roles', [])
        champion = Champion.objects.create(**validated_data)
        self._handle_roles(champion=champion, roles=roles)

        return champion

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles', [])

        if roles is not None:
            instance.role.clear()
            self._handle_roles(champion=instance, roles=roles)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
