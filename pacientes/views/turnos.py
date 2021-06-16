# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.views import generic

# Modelos
from ..models import Turno
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioTurno

class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos los turnos. 
    """
    model = Turno
    template_name = 'clinica/turnos/lista_turnos.html'
    context_object_name = 'Turnos'
    paginate_by = 5
    # page_kwarg

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Lista de turnos'
        contexto['buscar'] = 'Ingresa el nombre de alǵun paciente o una fecha'
        contexto['hoy'] = Turno.objects.filter(fecha=timezone.now()).filter(asistencia='P')
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo turno y retorna a la lista de turnos.
    """
    model = Turno
    form_class = FormularioTurno
    template_name = 'clinica/turnos/form_turno.html'
    success_url = reverse_lazy('pacientes:lista_turnos')


    def form_valid(self, form):
        registrarActividad(
            self.request,
            'Cargó un turno'
        )
        messages.success(
            self.request,
            'Turno cargado!'
        )
        form.instance.asistencia = Turno.ASISTIO_OPCIONES[0][0]  # P - PENDIENTE
        if not form.instance.fecha:
            form.instance.fecha = timezone.now()
        return super().form_valid(form)
 
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Registrar un nuevo turno'
        contexto['volver'] = self.success_url
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de una determinada observacion
    """
    model = Turno
    form_class = FormularioTurno
    template_name = 'clinica/turnos/form_turno.html'
    success_url = reverse_lazy('pacientes:lista_turnos')

    def form_valid(self, form):
        registrarActividad(
            self.request,
            'Modificó un turno'
        )
        messages.success(
            self.request,
            'Turno modificado!'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Turno para {self.object.paciente}'
        contexto['url_volver'] = self.success_url
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """
    Elimina un turno.
    """
    model = Turno
    template_name = 'componentes/delete.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un turno'
        )
        messages.success(
            self.request,
            'Turno eliminado!'
        )
        return reverse_lazy('pacientes:lista_turnos')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar el turno de {self.object.paciente}'
        contexto['url_volver'] = reverse_lazy('pacientes:lista_turnos')
        return contexto