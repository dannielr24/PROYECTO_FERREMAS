from django.db import models
from inventario_api.models import Producto

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_comprador = models.CharField(max_length=100, blank=True, null=True)
    email_comprador = models.EmailField(blank=True, null=True)
    telefono_comprador = models.CharField(max_length=20, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.total = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"