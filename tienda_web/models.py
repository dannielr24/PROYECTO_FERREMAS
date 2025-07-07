from django.db import models
from django.contrib.auth.models import User 
from inventario_api.models import Producto  
class Boleta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleta #{self.id} - Usuario: {self.usuario.username} - Total: ${self.total}"

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, related_name='detalles', on_delete=models.CASCADE)
    producto_id = models.IntegerField(default=0)  # Valor por defecto temporal
    nombre_producto = models.CharField(max_length=255, default="Producto desconocido")
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    imagen_url = models.URLField(blank=True, default="")
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.nombre_producto}"
