from django.db import models

class Pedido(models.Model):
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
