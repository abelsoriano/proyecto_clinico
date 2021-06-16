# Django
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django.forms.widgets import PasswordInput

# Modelos
from .models import Usuario

class FormularioUsuario(ModelForm):

    class Meta:
        model = Usuario
        fields = '__all__'
        widgets ={

        'password': PasswordInput(render_value=True,
                                      attrs={
                                          'placeholder': 'Ingrese su password',
                                      }
                                      ),
                                      
         
        }
        

        exclude = ['user_permissions', 'last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = Usuario.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data