# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic

# Modelos
from ..models import Pedido, Producto, DetallePedido
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioPedido

class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos los pedidos cargados en el sistema. 
    """
    model = Pedido
    template_name = 'clinica/pedidos/lista_pedidos.html'
    context_object_name = 'Pedidos'
    paginate_by = 5
    # page_kwarg

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Lista de pedidos'
        contexto['buscar'] = 'Ingresa el nombre de alǵun paciente'
        contexto['cantidad'] = Pedido.objects.all().count()
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo pedido y retorna a la lista de pacientes.
    """
    model = Pedido
    form_class = FormularioPedido
    template_name = 'clinica/pedidos/form_pedido.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Cargó un pedido'
        )
        messages.success(
            self.request,
            'Pedido cargado!'
        )
        ultimo = Pedido.objects.last()
        return reverse_lazy('productos:editar_pedido', kwargs={'pk': ultimo.id})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Agregar pedido'
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de un determinado pedido.
    """
    model = Pedido
    form_class = FormularioPedido
    template_name = 'clinica/pedidos/form_pedido.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Modificó un pedido'
        )
        messages.success(
            self.request,
            'Pedido modificado!'
        )
        return reverse_lazy('productos:lista_pedidos')            

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Pedido de {self.object.paciente}'
        contexto['cantidad'] = DetallePedido.objects.filter(pedido=self.kwargs['pk']).count()
        contexto['lista_productos'] = DetallePedido.objects.filter(pedido=self.kwargs['pk'])
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """ 
    Elimina un pedido del sistema.
    """
    model = Pedido
    template_name = 'componentes/delete.html'
    
    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un pedido'
        )
        messages.success(
            self.request,
            'Pedido eliminado!'
        )
        return reverse_lazy('productos:lista_pedidos')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object}'
        contexto['url_volver'] = reverse_lazy('productos:lista_pedidos')
        return contexto