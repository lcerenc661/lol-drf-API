"""League of legendes models"""

from django.db import models

# Create your models here.


class Role(models.Model):
    """Role model for the champions"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Champion(models.Model):
    """Basic league of legends champion model [Name, role, abilities]"""
    name = models.CharField(max_length=50)
    role = models.ManyToManyField(Role)

    def __str__(self):
        return self.name


class Ability(models.Model):
    """Abilities model, includes passives and definitives"""
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Champion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
