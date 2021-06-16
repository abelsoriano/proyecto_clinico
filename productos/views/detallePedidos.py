# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic

# Modelos
from ..models import DetallePedido, Pedido
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioDetallePedido


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo producto a la lista de productos de un pedido y puede 
    retornar a la lista o a un nuevo formulario para agregar otro producto más.
    """
    model = DetallePedido
    form_class = FormularioDetallePedido
    template_name = 'clinica/pedidos/detallePedido/form_detalle_pedido.html'

    def form_valid(self, form):
        registrarActividad(
            self.request,
            'Agregó un producto a un pedido'
        )
        messages.success(
            self.request,
            'Producto agregado al carrito!'
        )
        form.instance.pedido = Pedido.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('productos:editar_pedido', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        pedido = Pedido.objects.get(pk=self.kwargs['pk'])
        contexto = super().get_context_data(**kwargs)
        contexto['url_volver'] = self.get_success_url
        contexto['titulo'] = f'Pedido de {pedido.paciente}'
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de un determinado producto de la lista de compra.
    """
    model = DetallePedido
    form_class = FormularioDetallePedido
    template_name = 'clinica/pedidos/detallePedido/form_detalle_pedido.html'          

    def form_valid(self, form):
        registrarActividad(
            self.request,
            'Modificó los productos de un pedido'
        )
        messages.success(
            self.request,
            'Carrito actualizado!'
        )
        p = DetallePedido.objects.get(id=self.kwargs['pk'])
        form.instance.pedido = Pedido.objects.get(pk=p.pedido_id)
        return super().form_valid(form)

    def get_success_url(self):
        pedido = self.request.GET.get('pedido')
        return reverse_lazy('productos:editar_pedido', kwargs={'pk': pedido})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Producto para {self.object.pedido}'
        contexto['url_volver'] = self.get_success_url
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """
    Elimina un producto de la lista de compra.
    """
    model = DetallePedido
    template_name = 'componentes/delete.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un producto de un pedido'
        )
        messages.success(
            self.request,
            'Se elimino un producto del carrito!'
        )
        pedido = self.request.GET.get('pedido')
        return reverse_lazy('productos:editar_pedido', kwargs={'pk': pedido})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object}'
        # hago de vuelta esto porque si llamo a get_success_url me manda el mensaje 2 veces
        pedido = self.request.GET.get('pedido')
        contexto['url_volver'] = reverse_lazy('productos:editar_pedido', kwargs={'pk': pedido})
        return contexto