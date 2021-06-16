# Django
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils import timezone
from django.views import generic

# Modelos
from pacientes.models import Paciente, Turno
from productos.models import Pedido
from usuarios.models import Usuario
from .models import Filtro

# Formularios
from .forms import FiltroPacientes, FiltroMes

# Utils
from .utils import generar_reporte_pdf
 

pacientes = []
query_pacientes = 'Pacientes'


def todosLosPacientes():
    pacientes.clear()
    for p in Paciente.objects.all():
            pacientes.append(p)

class ListaPacientes(generic.ListView):
    """ Vista para generar reportes de pacientes. """
    context_object_name = 'pacientes'
    template_name = 'clinica/reportes/pacientes.html'

    def get_queryset(self):
        filtros = self.request.GET.get('filtros')
        todosLosPacientes()
        if filtros:
            q = Filtro.objects.get(id=filtros)
            fecha_actual = timezone.now().date()
            if q.filtro == 'Asistieron a los turnos en la semana/mes':
                query_pacientes = q.filtro
                pacientes.clear()
                turnos = Turno.objects.filter(
                    Q(fecha__month=fecha_actual.month) and Q(asistencia='A')
                )
                for turno in turnos:
                    paciente = Paciente.objects.get(id=turno.paciente.id)
                    pacientes.append(paciente)
            elif q.filtro == 'No asistieron a los turnos en la semana/mes':
                query_pacientes = q.filtro
                pacientes.clear()
                turnos = Turno.objects.filter(
                    Q(fecha__month=fecha_actual.month) and Q(asistencia='F')
                )
                for turno in turnos:
                    paciente = Paciente.objects.get(id=turno.paciente.id)
                    pacientes.append(paciente)
            elif q.filtro == 'Hicieron por lo menos un pedido en la semana/mes':
                query_pacientes = q.filtro
                pacientes.clear()
                pedidos = Pedido.objects.filter(created_at__month=fecha_actual.month)
                for pedido in pedidos:
                    paciente = Paciente.objects.get(id=pedido.paciente.id)
                    pacientes.append(paciente)
            elif q.filtro == 'Todos':
                query_pacientes = 'Pacientes'
                return pacientes
        return pacientes
        

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['form'] = FiltroPacientes
        contexto['titulo'] = 'Pacientes'
        return contexto 


ventas = []

class ListaVentasPorMes(generic.ListView):
    template_name = 'clinica/reportes/ventas.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        ventas.clear()
        mes = self.request.GET.get('meses')
        fecha_actual = timezone.now().date()
        vendedores = Usuario.objects.filter(rol='V')
        if mes:
            for v in vendedores:
                obj = {
                    'vendedor': v,
                    'cantidad': v.ventas.filter(
                        Q(estado='F') and Q(fecha_venta__month=int(mes))
                    ).count(),
                    'total': v.ventas.filter(
                        Q(estado='F') and Q(fecha_venta__month=int(mes))
                    ).aggregate(Sum('subtotal'))
                }
                ventas.append(obj)
            self.mes_total = fecha_actual.month
            return ventas
        else:
            for v in vendedores:
                obj = {
                    'vendedor': v,
                    'cantidad': v.ventas.filter(
                        Q(estado='F') and Q(fecha_venta__month=fecha_actual.month)
                    ).count(),
                    'total': v.ventas.filter(
                         Q(estado='F') and Q(fecha_venta__month=fecha_actual.month)
                    ).aggregate(Sum('subtotal'))
                }
                ventas.append(obj)
            return ventas

            
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['mes_total'] = self.request.GET.get('meses')
        contexto['titulo'] = 'Ventas'
        contexto['form'] = FiltroMes
        return contexto 


def descargarPDF(peticion):
    if peticion.method == 'GET':
        ruta = peticion.META.get('HTTP_REFERER')
        if 'ventas' in ruta:
            mes = ruta.split('=').pop()
            contexto = {
                'reporte': mes,
                'ventas': ventas,
                'titulo': f"Ventas del mes {mes}" 
            }
            pdf = generar_reporte_pdf(ListaVentasPorMes.template_name, contexto)
        else:
            contexto = {
                'reporte': query_pacientes,
                'pacientes': pacientes,
                'titulo':'Pacientes'
            }
            pdf = generar_reporte_pdf(ListaPacientes.template_name, contexto)
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponseRedirect(reverse_lazy('reportes:pacientes'))