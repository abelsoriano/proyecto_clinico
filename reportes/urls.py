# Django
from django.urls import path

# Vistas
from .views import ListaPacientes, ListaVentasPorMes, descargarPDF

app_name = 'reportes'

urlpatterns = [
    path('pacientes/',ListaPacientes.as_view(), name='pacientes'),
    path('ventas/', ListaVentasPorMes.as_view(), name='ventas'),
    path('descargar/', descargarPDF, name='descargar')
]