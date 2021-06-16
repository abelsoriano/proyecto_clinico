# Modelos
from django.contrib.auth.models import Group
from reportes.models import Filtro

def run():
    """ 
    Crea los grupos y filstros que necesita el sistema para funcionar. 
    > python manage.py runscript incial
    """
    Group.objects.bulk_create([
        Group(name="Medico"),
        Group(name="Secretaria"),
        Group(name="Gerencia"),
        Group(name="Venta"),
        Group(name="Taller")
    ])
    Filtro.objects.bulk_create([
        Filtro(filtro='Todos', recurso='Todos'),
        Filtro(filtro='Asistieron a los turnos en la semana/mes', recurso='Pacientes'),
        Filtro(filtro='No asistieron a los turnos en la semana/mes', recurso='Pacientes'),
        Filtro(filtro='Hicieron por lo menos un pedido en la semana/mes', recurso='Pacientes'),
    ])
