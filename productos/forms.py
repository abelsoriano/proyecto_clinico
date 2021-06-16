# Django
from django.forms import ModelForm

# Modelos
from .models import *
from usuarios.models import Usuario

class FormularioProducto(ModelForm):
    
    class Meta:
        model = Producto
        fields = '__all__'


class FormularioPedido(ModelForm):

    class Meta:
        model = Pedido
        fields = ('estado', 'paciente', 'tipo_de_pago', 'vendedor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendedor'].queryset = Usuario.objects.filter(rol='V')

#---------------------------------------
class FormularioDetallePedido(ModelForm):

    class Meta:
        model = DetallePedido
        fields = ('producto', 'cantidad')


class FormularioCategoria(ModelForm):

    class Meta:
        model = Categoria
        fields = '__all__'
