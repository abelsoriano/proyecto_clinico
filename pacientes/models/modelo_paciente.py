# Django
from django.db import models

# Modelos
from compartido.modelo_base import ModeloBase
from usuarios.models import Usuario


class Paciente(ModeloBase):
    """
    Esta clase contiene toda la lógica de los pacientes. 
    """
    nombre = models.CharField(max_length=25, verbose_name="Nombre")
    apellido = models.CharField(max_length=25, verbose_name="Apellido")
    edad = models.PositiveIntegerField(verbose_name="Edad")
    dni = models.CharField(max_length=11, unique=True, verbose_name="Documento", blank=True, null=True)
    telefono = models.TextField(verbose_name='Teléfono', blank=True, null=True )
    addres = models.CharField(max_length=66, verbose_name='Direcciòn')
    email = models.EmailField(blank=True, null=True, verbose_name="Correo")
    medico = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        verbose_name="Médico", 
        blank=True,
        null=True
    )
    imagen = models.ImageField(upload_to='pacientes/img/',blank=True, null=True, verbose_name="Imagen del paciente")
    record = models.ImageField(upload_to='record/img/',blank=True, null=True, verbose_name="Documento")

    class Meta:
        db_table = "paciente"
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['created_at']  
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

           



