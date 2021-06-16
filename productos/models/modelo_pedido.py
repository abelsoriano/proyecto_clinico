# Python
from decimal import Decimal

# Django
from django.db import models
from django.utils import timezone

# Modelos
from compartido.modelo_base import ModeloBase
from pacientes.models import Paciente
from .modelo_producto import Producto
from usuarios.models import Usuario


class Pedido(ModeloBase):
    """
    Esta clase contiene la logica para persistir pedidos en el sistema.
    El rol de ventas es el encargado de generar los pedidos.
    """

    OPCIONES_ESTADO = (
    ('P', 'Pendiente'),
    ('T', 'Almacen'),
    ('F', 'Finalizado'),
    )

    OPCIONES_DE_PAGO = (
        ('TC', 'Tarjeta de credito'),
        ('BV', 'Billetera virtual'),
        ('EF', 'Efectivo'),
        ('DE', 'Debito'),
    )

    estado = models.CharField(
        max_length=1,
        default='P',
        choices=OPCIONES_ESTADO,
        verbose_name="Estado actual del pedido"
    )
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, verbose_name="Paciente")
    subtotal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.0,
        verbose_name="Sub-total",
        blank=True,
        null=True
    )
    tipo_de_pago = models.CharField(
        max_length=2,
        default='TC',
        choices=OPCIONES_DE_PAGO,
        verbose_name='Tipo de pago'
    )
    vendedor = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        verbose_name='Vendedor responsable del pedido',
        related_name="ventas",
        blank=True,
        null=True
    )
    fecha_venta = models.DateField(verbose_name="Fecha", blank=True, null=True)

    class Meta:
        db_table = 'pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.estado == 'F':
            self.fecha_venta = timezone.now()
        super().save(*args, **kwargs)

    def verSubTotal(self):
        return f"$ {self.subtotal}"

    def __str__(self):
        return f"{self.paciente.nombre} {self.paciente.apellido}, {self.get_estado_display()}"



class DetallePedido(ModeloBase):
    """
    Tabla intermedia entre los pedidos y sus productos
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad", default=1)
    total = models.DecimalField(max_digits=14,
                                decimal_places=2,
                                default=0.0,
                                blank=True,
                                verbose_name="Total del detalle" )

    def save(self, *args, **kwargs):
        """
        Cuando se agregue un producto a la lista de compra, se actualiza
        el precio total y el stock.
        """
        self.total = self.producto.precio * Decimal(self.cantidad)  # monto
        producto = Producto.objects.get(id=self.producto.id)
        pedido = Pedido.objects.get(id=self.pedido.id)
        # En caso de actualziar el detalle
        detalle = DetallePedido.objects.filter(id=self.id)
        if detalle:
            # Más productos
            if self.cantidad > detalle[0].cantidad:
                # Total
                pedido.subtotal += self.total - detalle[0].total
                # Stock
                producto.stock  -= detalle[0].cantidad - self.cantidad
            # Menos productos
            else:
                # Total
                pedido.subtotal -= detalle[0].total - self.total
                # Stock
                producto.stock  += self.cantidad - detalle[0].cantidad
        else:
           # Actualizo el precio
            if pedido.subtotal:
                pedido.subtotal += self.total
            else:
                pedido.subtotal = self.total
            # Actualizo el stock
            producto.stock -= self.cantidad
        producto.save()
        pedido.save()
        super().save(*args, **kwargs)



    def delete(self, *args, **kwargs):
        """
        Cuando se elimine un producto de la lista de compra, se actualiza el precio total y el stock
        """
        # Actualizo el precio
        pedido = Pedido.objects.get(id=self.pedido.id)
        pedido.subtotal -= self.total
        pedido.save()
        # Actualizaco el stock
        producto = Producto.objects.get(id=self.producto.id)
        producto.stock += self.cantidad
        producto.save()
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle del pedido'
        verbose_name_plural = 'Detalles de pedidos'

    def obtenerCantidad(self):
        return f"{self.cantidad} {'unidades' if self.cantidad > 1 else 'unidad'}"

    def __str__(self):
        return self.producto.nombre
