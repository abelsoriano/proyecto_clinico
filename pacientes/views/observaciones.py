# Django
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Modelos
from ..models import Observacion, Paciente
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioObservacion


class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos las observaciones de un paciente en el sistema. 
    """
    template_name = 'clinica/pacientes/observaciones/lista_observaciones.html'
    context_object_name = 'Observaciones'
    paginate_by = 5
    # page_kwarg

    def get_queryset(self):
        return Observacion.objects.filter(paciente=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        paciente = Paciente.objects.get(id=self.kwargs['pk'])
        contexto = super().get_context_data(**kwargs)
        contexto['pacienteid'] = paciente.id
        contexto['titulo'] = f'Historial médico de {paciente}'
        contexto['cantidad'] = Observacion.objects.filter(paciente=self.kwargs['pk']).count()
        contexto['volver'] = reverse_lazy('pacientes:detalle', kwargs={'pk':self.kwargs['pk']})
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega una nueva observación al historial de un paciente.
    """
    model = Observacion
    form_class = FormularioObservacion
    template_name = 'clinica/pacientes/observaciones/form_observacion.html'

    def form_valid(self, form):
        registrarActividad(
            self.request,
            'Cargo una observación'
        )
        messages.success(
            self.request,
            'Observación cargada!'
        )
        form.instance.paciente = Paciente.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pacientes:lista_observaciones', kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Agregar nueva observación'
        contexto['url_volver'] = self.get_success_url
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de una determinada observacion
    """
    model = Observacion
    form_class = FormularioObservacion
    template_name = 'clinica/pacientes/observaciones/form_observacion.html'          

    def form_valid(self, form):
        registrarActividad(
            self.request,
            'Modifico una observación'
        )
        messages.success(
            self.request,
            'Observación modificada!'
        )
        paciente = Paciente.objects.get(id=self.request.GET.get('paciente'))
        form.instance.paciente = Paciente.objects.get(pk=paciente.id)
        return super().form_valid(form)

    def get_success_url(self):
        uuid = self.request.GET.get('paciente')
        paciente = Paciente.objects.get(id=uuid)
        return reverse_lazy('pacientes:lista_observaciones', kwargs={'pk': paciente.id})

    def get_context_data(self, **kwargs):
        paciente = Paciente.objects.get(id=self.request.GET.get('paciente'))
        contexto = super().get_context_data(**kwargs)
        contexto['pacienteid'] = paciente.id
        contexto['titulo'] = f'Observación de {self.object.paciente}'
        contexto['url_volver'] = self.get_success_url
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """
    Elimina una observacion del historial de un paciente
    """
    model = Observacion
    template_name = 'componentes/delete.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó una observación'
        )
        messages.success(
            self.request,
            'Observación eliminada!'
        )
        lista = self.request.GET.get('lista')
        return reverse_lazy('pacientes:lista_observaciones', kwargs={'pk': lista})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object.motivo_consulta}'
        contexto['url_volver'] = reverse_lazy('pacientes:lista_observaciones', kwargs={'pk': lista})
        return contexto