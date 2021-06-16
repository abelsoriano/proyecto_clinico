# Django
from django.db import models
from django.utils import timezone

# Modelos
from compartido.modelo_base import ModeloBase
from . import Paciente

class Hora(ModeloBase):
    hora_cit = models.TextField(max_length=15)

    def __str__(self):
        return self.hora_cit

class Turno(ModeloBase):
    """
    Esta clase contiene la logica para persistir turnos en el sistema.
    El rol de Secretaria/Secretario es el encargado de administrar los pedidos.
    """
    
    ASISTIO_OPCIONES = (
        ('P', 'Pendiente'),
        ('A', 'Asistió'),
        ('F', 'Faltó')
    )

    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        verbose_name="Paciente",
        related_name="turnos"
    ) 
    asistencia = models.CharField(
        max_length=1, 
        choices=ASISTIO_OPCIONES,  
        verbose_name="Asistencia",
        blank=True,
        null=True
    )
    time = models.ForeignKey(Hora, on_delete=models.CASCADE, verbose_name="Hora de la Cita")
    fecha = models.DateField(verbose_name="Día")


    class Meta:
        db_table = "turno"
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
    
    def __str__(self):
        return f"{self.paciente.nombre} {self.paciente.apellido}, {self.fecha}"
