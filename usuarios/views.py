# Django
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.timezone import localtime, now
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import DeleteView, UpdateView


# Modelos
from .models import Usuario, ROL_OPCIONES, Actividad
from django.contrib.auth.models import Group
from usuarios.models import registrarActividad

# Formularios
from .forms import FormularioUsuario

class IniciarSesion(LoginView):
    template_name = 'clinica/usuarios/inicio_de_sesion.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('compartido:inicio')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        usuario = self.request.user.username
        ultima_vez = localtime(self.request.user.last_login).date()
        fecha_registro = localtime(self.request.user.date_joined).date()
        if fecha_registro == ultima_vez:
            messages.success(
                self.request,
                f'Hola {usuario}! que tengas un productivo primer dia en el sistema! 🥳'
            )
        else:
            messages.success(
                self.request,
                f'Hola {usuario}! entraste por ultima vez el {ultima_vez}'
            )
        if self.request.user.groups.exists():
            grupo = self.request.user.groups.get()
            if grupo.name == ROL_OPCIONES[0][1]:
                # Medico
                return reverse_lazy('pacientes:lista')
            elif grupo.name == ROL_OPCIONES[1][1]:  
                # SECRETARIA
                return reverse_lazy('pacientes:lista_turnos')
            elif grupo.name == ROL_OPCIONES[2][1]:  
                # Gerencia
                return reverse_lazy('productos:lista')
            elif grupo.name == ROL_OPCIONES[3][1]:  
                # Venta
                return reverse_lazy('productos:lista_pedidos')
            elif grupo.name == ROL_OPCIONES[4][1]:  
                # Taller
                return reverse_lazy('productos:lista_pedidos')
        return reverse_lazy('productos:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Iniciar Sesión'
        return ctx


class CrearUsuario(generic.CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'clinica/usuarios/form_usuario.html'
    # permission_required = 'user.add_user'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('compartido:inicio')
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_staff = True
        form.instance.is_active = True
        return super().form_valid(form)
    
    def get_success_url(self):
        nombre_usuario = self.request.POST.get('username')
        usuario = Usuario.objects.get(username=nombre_usuario)
        grupo = Group.objects.get(name=usuario.get_rol_display())
        usuario.groups.add(grupo.id)
        messages.success(
            self.request,
            f'Usuario {nombre_usuario} registrado!'
        )
        return reverse_lazy('usuarios:listar')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Crear usuario'
        return ctx


class ListaActividades(generic.ListView):
    queryset = Actividad.objects.order_by('-id')
    template_name = 'clinica/usuarios/actividades.html'
    context_object_name = 'Actividades'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Registro de actividades'
        ctx['buscar'] = 'Nombre de usuario o actividad'
        return ctx


class ListaUsuarios(generic.ListView):
    queryset = Usuario.objects.order_by('-date_joined')
    template_name = 'clinica/usuarios/lista_usuarios.html'
    context_object_name = 'Usuarios'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Lista de usuarios'
        ctx['buscar'] = 'Nombre de usuario o sector'
        return ctx


class EditUsuario(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'clinica/usuarios/form_usuario.html'
    success_url = reverse_lazy('usuarios:lista')
    permission_required = 'user.change_user'
    permission_required = 'user.add_user'
    url_redirect = success_url

    def form_valid(self, form):
        form.instance.is_staff = True
        form.instance.is_active = True
        return super().form_valid(form)
    
    def get_success_url(self):
        nombre_usuario = self.request.POST.get('username')
        usuario = Usuario.objects.get(username=nombre_usuario)
        grupo = Group.objects.get(name=usuario.get_rol_display())
        usuario.groups.add(grupo.id)
        messages.success(
            self.request,
            f'Usuario {nombre_usuario} actualizado!'
        )
        return reverse_lazy('usuarios:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editando Usuario'
        return ctx

class EliminarUsuario(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'clinica/usuarios/delete.html'
    success_url = reverse_lazy('usuarios:lista')
    permission_required = 'user.delete_user'
    url_redirect = success_url

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         self.object.delete()
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminando  un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context