from django.db import models

class Pedido(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    cliente = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    direccion = models.CharField(max_length=200)
    estado = models.CharField(max_length=50, default='pendiente')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.producto} x {self.cantidad} para {self.cliente}"
