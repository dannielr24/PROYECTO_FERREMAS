# pedido_api/models.py
from django.db import models
from inventario_api.models import Producto

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pedidos_pedido_api')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
