# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Q
from django.views import generic

# Modelos
from ..models import Producto, Categoria
from usuarios.models import registrarActividad

# Formularios
from ..forms import FormularioProducto


class Listar(LoginRequiredMixin, generic.ListView):
    """
    Lista todos los productos cargados en el sistema. 
    """
    model = Producto
    template_name = 'clinica/productos/lista_productos.html'
    context_object_name = 'Productos'
    paginate_by = 5
    # page_kwarg

    def get_queryset(self):
        q_busqueda = self.request.GET.get('query')
        q_categoria_nombre = self.request.GET.get('categoria')
        if q_busqueda:
            return Producto.objects.filter(
                Q(nombre__in=q_busqueda.split()) | Q(nombre__icontains=q_busqueda.split()[0])
            )
        if q_categoria_nombre:
            q_categoria = Categoria.objects.get(nombre=q_categoria_nombre)
            return Producto.objects.filter(categoria=q_categoria.id)    
        return Producto.objects.all()

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Lista de productos'
        contexto['buscar'] = 'Ingresa el nombre de alǵun producto'
        contexto['cantidad'] = Producto.objects.all().aggregate(Sum('stock')).get('stock__sum')
        contexto['categorias'] = Categoria.objects.all()
        return contexto


class Agregar(LoginRequiredMixin, generic.CreateView):
    """ 
    Agrega un nuevo producto y retorna a la lista de pacientes.
    """
    model = Producto
    form_class = FormularioProducto
    template_name = 'clinica/productos/form_producto.html'
    success_url = reverse_lazy('productos:lista')

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Cargó un producto'
        )
        messages.success(
            self.request,
            'Producto cargado!'
        )
        path_previo = self.request.GET.get('prev')
        # Si accedemos desde detalle pedido, volverá al detalle
        if path_previo:
            pedido_id = path_previo.split('/').pop()
            return reverse_lazy('productos:agregar_detalle', kwargs={'pk':pedido_id})
        else:
            # Si no, vuelve a lista de productos
            return reverse_lazy('productos:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = 'Agregar producto'
        return contexto



class Detalle(LoginRequiredMixin, generic.DetailView):
    """ 
    Muestra toda la información de un determinado producto.
    """
    model = Producto
    template_name = 'clinica/productos/detalle_producto.html'
    context_object_name = 'Producto'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = self.object
        contexto['cantidad'] = Producto.objects.count()
        return contexto


class Editar(LoginRequiredMixin, generic.UpdateView):
    """ 
    Modifica la información de un determinado producto.
    """
    model = Producto
    form_class = FormularioProducto
    template_name = 'clinica/productos/form_producto.html'

    def get_success_url(self):
        registrarActividad(
            self.request,
            'Modificó un producto'
        )
        messages.success(
            self.request,
            'Producto modificado!'
        )
        ruta = self.request.META['HTTP_REFERER']
        producto_uuid = ruta.split('/').pop()
        return reverse_lazy('productos:detalle', kwargs={'pk': producto_uuid})

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Editar a {self.object}'
        contexto['editar'] = True
        return contexto


class Eliminar(LoginRequiredMixin, generic.DeleteView):
    """ 
    Elimina un producto del sistema.
    """
    model = Producto
    template_name = 'componentes/delete.html'
    
    def get_success_url(self):
        registrarActividad(
            self.request,
            'Eliminó un producto'
        )
        messages.success(
            self.request,
            'Producto eliminado!'
        )
        return reverse_lazy('productos:lista')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = f'Eliminar {self.object}'
        contexto['url_volver'] = reverse_lazy('productos:lista')
        return contexto