# Django
from django.urls import path

# Vistas

from .views import pacientes, observaciones, turnos

app_name = 'pacientes'

URLS_PACIENTES = [
    path('', pacientes.Listar.as_view(), name='lista'),
    path('agregar/', pacientes.Agregar.as_view(), name='agregar'),
    path('detalle/<uuid:pk>', pacientes.Detalle.as_view(), name='detalle'),
    path('editar/<uuid:pk>', pacientes.Editar.as_view(), name='editar'),
    path('eliminar/<uuid:pk>', pacientes.Eliminar.as_view(), name='eliminar'),
]

URL_OBSERVACIONES = [
    path('observaciones/<uuid:pk>', observaciones.Listar.as_view(), name='lista_observaciones'),
    path('observaciones/agregar/<uuid:pk>', observaciones.Agregar.as_view(), name='agregar_observacion'),
    path('observaciones/editar/<uuid:pk>', observaciones.Editar.as_view(), name='editar_observacion'),
    path('observaciones/eliminar/<uuid:pk>', observaciones.Eliminar.as_view(), name='eliminar_observacion')
]

URL_TURNOS = [
    path('turnos/', turnos.Listar.as_view(), name='lista_turnos'),
    path('turnos/agregar', turnos.Agregar.as_view(), name='agregar_turno'),
    path('turnos/editar/<uuid:pk>', turnos.Editar.as_view(), name='editar_turno'),
    path('turnos/eliminar/<uuid:pk>', turnos.Eliminar.as_view(), name='eliminar_turno')
]

urlpatterns = URLS_PACIENTES + URL_OBSERVACIONES + URL_TURNOS
