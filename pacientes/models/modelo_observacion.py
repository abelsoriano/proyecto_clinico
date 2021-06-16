# Django
from django.db import models

# Modelos
from compartido.modelo_base import ModeloBase
from .modelo_paciente import Paciente

class Observacion(ModeloBase):
    """
    Solo un Profesional médico debe agregar observaciones al historial de cada paciente.
    El conjunto de observaciones de cada paciente crea su historial médico.
    """
    motivo_consulta = models.CharField(max_length=100, verbose_name="Motivo")
    descripcion = models.TextField(verbose_name="Observación", blank=True, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente", related_name="observaciones", blank=True, null=True)

    class Meta:
        db_table = 'observacion'
        verbose_name = 'Observación'
        verbose_name_plural = 'Observaciones'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.paciente}, {self.motivo_consulta}"