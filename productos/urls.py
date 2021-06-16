# Django
from django.urls import path

# Vistas
from .views import productos, pedidos, detallePedidos as detalles, categorias

app_name = 'productos'

URLS_PRODUCTOS = [
    path('', productos.Listar.as_view(), name='lista'),
    path('agregar/', productos.Agregar.as_view(), name='agregar'),
    path('detalle/<uuid:pk>', productos.Detalle.as_view(), name='detalle'),
    path('editar/<uuid:pk>', productos.Editar.as_view(), name='editar'),
    path('eliminar/<uuid:pk>', productos.Eliminar.as_view(), name='eliminar'),
]

URLS_CATEGORIAS = [
    path('categorias/', categorias.Agregar.as_view(), name='categorias'),
    path('categorias/editar/<int:pk>', categorias.Editar.as_view(), name='editar_categoria'),
    path('categorias/eliminar/<int:pk>', categorias.Eliminar.as_view(), name='eliminar_categoria')
]


URLS_PEDIDOS = [
    path('pedidos/', pedidos.Listar.as_view(), name='lista_pedidos'),
    path('pedidos/agregar/', pedidos.Agregar.as_view(), name='agregar_pedido'),
    path('pedidos/editar/<uuid:pk>', pedidos.Editar.as_view(), name='editar_pedido'),
    path('pedidos/eliminar/<uuid:pk>', pedidos.Eliminar.as_view(), name='eliminar_pedido')
]

URLS_DETALLES = [
    path('pedidos/agregar_producto/<uuid:pk>', detalles.Agregar.as_view(), name='agregar_detalle'),
    path('pedidos/eliminar_producto/<uuid:pk>', detalles.Eliminar.as_view(), name='eliminar_detalle'),
    path('pedidos/editar_producto/<uuid:pk>', detalles.Editar.as_view(), name='editar_detalle')
]

urlpatterns = URLS_PRODUCTOS + URLS_CATEGORIAS + URLS_PEDIDOS + URLS_DETALLES