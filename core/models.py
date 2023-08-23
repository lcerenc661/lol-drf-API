from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Champion(models.Model):
    name = models.CharField(max_length=50)
    role = models.ManyToManyField(Role)

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Champion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
