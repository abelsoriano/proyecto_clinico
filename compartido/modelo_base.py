# Python
from uuid import uuid4

# Django
from django.db import models


class ModeloBase(models.Model):
    """
    Esta clase contiene los campos que son comunes en todas
    las demás clases. 
    """
    id = models.UUIDField(primary_key=True,
                          default=uuid4,
                          editable=False,
                          verbose_name="UUID"
                          )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Creación")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Última actualización")

    class Meta:
        abstract = True