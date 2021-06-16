# Django
from django import  *
from django.db.models.fields import CharField, IntegerField, PositiveIntegerField, PositiveSmallIntegerField, TimeField
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import DateInput, Input, TextInput, TimeInput

# Modelos
from .models import *
from usuarios.models import Usuario

from pacientes import models


class FormularioPaciente(ModelForm):

    class Meta:
        model = Paciente
        fields = '__all__'
        widgets={
            'telefono': TextInput(attrs={
                'autocomplete': 'off',
                'id': 'phone',
                'class': 'form-control rounded-pill ', 
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].queryset = Usuario.objects.filter(rol='M')

#--------------------------------------
class FormularioObservacion(ModelForm):

    class Meta:
        model = Observacion
        fields = '__all__'

# -------------------------------
class FormularioTurno(ModelForm):

    class Meta:
        model = Turno
        fields = '__all__'
        widgets={
            'fecha' : DateInput(attrs={
            'class': 'form-control rounded-pill ',    
            'autocomplete': 'off',
            'id': 'datepicker',
            'formats': '%d-%m-%Y'                
            }),

            # 'time': TimeInput(attrs={
            #     'autocomplete': 'off',
            #     'id': 'selector',
            #     'format': 'xxx-xxx-xxxxx'
            # })


        }
