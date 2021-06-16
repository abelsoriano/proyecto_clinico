# Python
from datetime import date

# Django
from django.db import models

# Modelos
from compartido.modelo_base import ModeloBase


class Categoria(models.Model):
    nombre = models.CharField(max_length=250, verbose_name="Nombre de la categoria")

    class Meta:
        db_table = "categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Producto(ModeloBase):
    """ 
    Esta clase contiene la logica para persistir productos en el sistema.
    """

    LADO_OPCIONES = (
        ('izquierdo', 'Izquierdo'),
        ('derecho', 'Derecho')
    )

    DISTANCIA_OPCIONES = (
        ('lejos', 'Lejos'),
        ('cerca', 'Cerca')
    )

    nombre = models.CharField(max_length=250, verbose_name="Nombre", unique=True)
    cod_producto = models.CharField(max_length=100, verbose_name="Código del producto", blank=True, null=True)
    precio = models.DecimalField(max_digits=14, decimal_places=2, default=0.0, verbose_name="Precio")
    imagen = models.ImageField(upload_to='productos/img/', blank=True, null=True, verbose_name="Imagen del producto")
    stock = models.PositiveIntegerField(blank=True, null=True, verbose_name="Cantidad", default=1)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        blank=True,
        null=True,
        verbose_name="Categoria",
        )
    armazon = models.BooleanField(default=False, verbose_name="Armazon")
    lente = models.BooleanField(default=False, verbose_name="Es un lente")
    lado = models.CharField(
        max_length=9,
        choices=LADO_OPCIONES,
        default='izquierdo',
        blank=True,
        null=True,
        verbose_name="Para que ojo"
        )
    distancia = models.CharField(
        max_length=5,
        choices=DISTANCIA_OPCIONES,
        default='lejos',
        blank=True,
        null=True,
        verbose_name="Distancia"
    )
        
    class Meta:
        db_table = "producto"
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.lente == False:
            self.distancia = None
            self.lado = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} | stock: {self.stock} | $ {self.precio} "