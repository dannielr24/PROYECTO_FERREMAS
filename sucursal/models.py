from django.db import models
from inventario_api.models import Producto  # Asegúrate de que esto funcione según tu estructura

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100, default='Santiago')
    region = models.CharField(max_length=100, default='Metropolitana')

    def __str__(self):
        return self.nombre

class InventarioSucursal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'sucursal')

class TransferenciaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='transferencias_salida')
    sucursal_destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='transferencias_entrada')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        inventario_origen = InventarioSucursal.objects.get(producto=self.producto, sucursal=self.sucursal_origen)
        if inventario_origen.stock < self.cantidad:
            raise ValueError("Stock insuficiente en la sucursal origen.")
        inventario_origen.stock -= self.cantidad
        inventario_origen.save()

        inventario_destino, created = InventarioSucursal.objects.get_or_create(
            producto=self.producto,
            sucursal=self.sucursal_destino,
            defaults={'stock': 0}
        )
        inventario_destino.stock += self.cantidad
        inventario_destino.save()

        super().save(*args, **kwargs)
