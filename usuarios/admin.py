# Django
from django.contrib import admin

# Modelos
from .models import Usuario, Actividad

admin.site.register(Usuario)
admin.site.register(Actividad)