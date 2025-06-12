from rest_framework import viewsets
from .models import Sucursal, InventarioSucursal, TransferenciaProducto
from .serializers import SucursalSerializer, InventarioSucursalSerializer, TransferenciaProductoSerializer

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer

class InventarioSucursalViewSet(viewsets.ModelViewSet):
    queryset = InventarioSucursal.objects.all()
    serializer_class = InventarioSucursalSerializer

class TransferenciaProductoViewSet(viewsets.ModelViewSet):
    queryset = TransferenciaProducto.objects.all()
    serializer_class = TransferenciaProductoSerializer

    def perform_create(self, serializer):
        transferencia = serializer.save()

        # Actualizar stock en la sucursal de origen
        inventario_origen = InventarioSucursal.objects.get(
            sucursal=transferencia.sucursal_origen,
            producto=transferencia.producto
        )
        inventario_origen.stock -= transferencia.cantidad
        if inventario_origen.stock < 0:
            inventario_origen.stock = 0  # No permitir stock negativo
        inventario_origen.save()

        # Actualizar stock en la sucursal de destino
        inventario_destino, created = InventarioSucursal.objects.get_or_create(
            sucursal=transferencia.sucursal_destino,
            producto=transferencia.producto,
            defaults={'stock': 0}
        )
        inventario_destino.stock += transferencia.cantidad
        inventario_destino.save()

        # (Opcional) Actualizar el stock general del producto para ventas
        producto = transferencia.producto
        # Calcular el stock total sumando inventarios de todas las sucursales
        stock_total = sum(inv.stock for inv in InventarioSucursal.objects.filter(producto=producto))
        producto.stock_disponible = stock_total
        producto.save()
