# Django
from django.db import models

class Filtro(models.Model):
    filtro = models.CharField(max_length=200, verbose_name="Filtro")
    recurso = models.CharField(max_length=200, verbose_name="Recurso")

    def __str__(self):
        return self.filtro