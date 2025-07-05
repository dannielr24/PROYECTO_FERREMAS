# inventario_api/models.py
from django.db import models

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, default='000000')   # Código único para el producto
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_disponible = models.PositiveIntegerField(default=0)
    
    # Campo para subir imágenes reales:
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pedidos_inventario_api')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    # Datos del comprador
    nombre_comprador = models.CharField(max_length=100, blank=True, null=True)
    email_comprador = models.EmailField(blank=True, null=True)
    telefono_comprador = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} pedido por {self.nombre_comprador}"