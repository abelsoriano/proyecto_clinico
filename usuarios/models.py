# Django
from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

# Modelos
from django.contrib.auth.models import AbstractUser, Group

ROL_OPCIONES = (
    ('M', 'Medico'),  
    ('S', 'Secretaria'),  
    ('G', 'Gerencia'), 
    ('V', 'Venta'), 
    ('T', 'Taller') 
)

class Usuario(AbstractUser):
    imagen = models.ImageField(upload_to='usuarios/img', blank=True, null=True, verbose_name="Imagen")
    rol = models.CharField(max_length=1, default='S', choices=ROL_OPCIONES, verbose_name="Sector")
    dni = models.CharField(max_length=11, verbose_name="Documento")
    # nombre = models.CharField(max_length=25, verbose_name="Nombre")
    # apellido = models.CharField(max_length=25, verbose_name="Apellido")
    ultima_actividad = models.DateTimeField(verbose_name="Última actividad", blank=True, null=True)

    

    def __str__(self):
        return self.first_name +' '+ self.last_name
    
    # def toJSON(self):
    #     item = model_to_dict(self, exclude=['password','user_permissions', 'last_login'])
    #     if self.last_login:
    #         #  item['last_login'] = self.last_login.strftime('%Y-%m-%d')
    #     # item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
    #     # item['image'] = self.get_image()
    #     item['full_name'] = self.get_full_name()
    #     item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
    #     return item


class Actividad(models.Model):
    """
    Cada interación con el sistema por parte de los empleados
    registrará una nueva actividad. 
    """
    accion = models.CharField(max_length=100, verbose_name="Acción")
    # No hago una relación con usuarios porque solo quiero registrar el nombre
    # y que persista independientemente de que el usuario sea borrado.
    # Si pongo on_delete=models.SET_NULL lo mismo necesitaria este campo.
    # Directamente uso solo este campo
    usuario = models.CharField(max_length=100, verbose_name="Usuario")
    momento = models.DateTimeField(verbose_name="Momento de la acción")

    def __str__(self):
        return self.acccion


def registrarActividad(request, mensaje):
    u_username = request.user.username
    u_nombre = f'{request.user.first_name} {request.user.last_name}'
    u_dni = request.user.dni
    usuario_actual = f'{u_username}, {u_nombre}, {u_dni}'
    accion_actual = mensaje
    Actividad.objects.create(accion=accion_actual, usuario=usuario_actual, momento=timezone.now())
    usuario_actual = Usuario.objects.get(id=request.user.id)
    usuario_actual.ultima_actividad = timezone.now()
    usuario_actual.save()