# Django
from django.db.models import Q
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Modelos
from ..models import Paciente, Turno
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioPaciente


class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos los pacientes cargados en el sistema. 
    """
    template_name = 'clinica/pacientes/lista_pacientes.html'
    context_object_name = 'Pacientes'
    paginate_by = 5
    # page_kwarg

    def get_queryset(self):
        b_query = self.request.GET.get('query')
        b_fecha = self.request.GET.get('fecha')
        if self.request.user.rol == 'M':
            if b_fecha:
                data = []  # Pacientes que fueron atendidos esa fecha por ese doctor
                turnos = Turno.objects.filter(fecha=b_fecha).filter(asistencia='A')
                for turno in turnos:
                    paciente = Paciente.objects.get(id=turno.paciente.id)
                    if paciente.medico == self.request.user:
                        data.append(paciente)
                return data
            if b_query:
                return Paciente.objects.filter(
                    # Busco ocurrencias...
                    Q(nombre__in=b_query.split()) | Q(apellido__in=b_query.split()) |
                    Q(nombre__icontains=b_query.split()[0])  |
                    Q(apellido__icontains=b_query.split()[0])|
                    Q(dni__contains=b_query)
                ).filter(medico=self.request.user.id)
            else:
                return Paciente.objects.filter(medico=self.request.user.id)            
        if b_fecha:
            data = []  # Pacientes que fueron atendidos esa fecha
            turnos = Turno.objects.filter(fecha=b_fecha).filter(asistencia='A')
            for turno in turnos:
                paciente = Paciente.objects.get(id=turno.paciente.id)
                data.append(paciente)
            if len(data)==0:
                messages.error(
                    self.request,
                    f"Ningún paciente fue atendido el dia {b_fecha}"
                )
            return data
        if b_query:
            return Paciente.objects.filter(
                # Busco ocurrencias...
                Q(nombre__in=b_query.split()) | Q(apellido__in=b_query.split()) |
                Q(nombre__icontains=b_query.split()[0])  |
                Q(apellido__icontains=b_query.split()[0])|
                Q(dni__contains=b_query)  
            )
        else:
            return Paciente.objects.all()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Lista de pacientes'
        contexto['buscar'] = 'Ingresa el nombre de algún paciente o el DNI'
        contexto['cantidad'] = Paciente.objects.count()
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo paciente y retorna a la lista de pacientes.
    """
    model = Paciente
    form_class = FormularioPaciente
    template_name = 'clinica/pacientes/form_paciente.html'

    def form_valid(self, form):
        registrarActividad(
            self.request, 
            'Cargó un paciente'
        )
        # Mensaje al usuario
        messages.success(
            self.request,
            'Paciente cargado!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        path_previo = self.request.GET.get('prev')
        if path_previo:
            # Si accedemos desde pedidos, volverá a pedidos
            if 'pedidos' in path_previo:
                return reverse_lazy('productos:agregar_pedido')
            # Si accedemos desde cargar turno, volverá a cargar turnos
            if 'turnos' in path_previo:
                return reverse_lazy('pacientes:agregar_turno')
            # Si no, vuelve a lista de pacientes
        else:
            return reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Agregar nuevo paciente'
        contexto['volver'] = self.get_success_url
        return contexto


class Detalle(LoginRequiredMixin, generic.DetailView):
    """ 
    Muestra toda la información de un determinado paciente.
    """
    model = Paciente
    template_name = 'clinica/pacientes/detalle_paciente.html'
    context_object_name = 'Paciente'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = self.object
        contexto['Historial'] = self.object.observaciones.all().order_by('-created_at')[0:6]
        contexto['cantidad'] = self.object.observaciones.count()
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de un determinado paciente.
    """
    model = Paciente
    form_class = FormularioPaciente
    template_name = 'clinica/pacientes/form_paciente.html'

    def get_success_url(self):
        registrarActividad(
            self.request, 
            'Modificó un paciente'
        )
        # Mensaje al usuario
        messages.success(
            self.request,
            'Paciente modificado!'
        )
        return reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Editar a {self.object}'
        contexto['volver'] = reverse_lazy('pacientes:detalle', kwargs={'pk':self.kwargs['pk']})
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """ 
    Elimina un determinado paciente del sistema.
    """
    model = Paciente
    template_name = 'componentes/delete.html'
    
    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un paciente'
        )
        # Mensaje al usuario
        messages.success(
            self.request,
            'Paciente eliminado!'
        )
        return reverse_lazy('pacientes:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar a {self.object}'
        contexto['url_volver'] = reverse_lazy('pacientes:lista')
        return contexto