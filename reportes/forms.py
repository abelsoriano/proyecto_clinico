# Django
from django import forms
from django.db.models import Q

# Modelos
from .models import Filtro

class FiltroPacientes(forms.Form):
    filtros = forms.ModelChoiceField(queryset=Filtro.objects.filter(
        Q(recurso='Pacientes')|Q(recurso='Todos')), label=''
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['filtros'].widget.attrs['class'] = 'form-control mt-2 rounded' 

    class Meta:
        fields = ['filtros']

class FiltroMes(forms.Form):
    """ Firefox no soporta el input de tipo month xd """
    MESES = (
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre')
    )
    meses = forms.ChoiceField(choices=MESES, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meses'].widget.attrs['class'] = 'form-control mt-2 rounded'