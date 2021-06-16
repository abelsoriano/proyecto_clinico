# Django
from django.contrib import admin

# Modelos
from .models import *

@admin.register(Producto, Pedido, DetallePedido)
class AplicacionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Categoria)