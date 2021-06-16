# Django
from pacientes.models.modelo_turno import Hora
from django.contrib import admin

# Modelos
from .models import *

@admin.register(Paciente, Observacion, Turno, Hora )
class AplicacionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')