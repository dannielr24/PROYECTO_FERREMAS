from rest_framework import viewsets, status
from rest_framework.response import Response
from control_api.models import Pedido
from control_api.serializers import PedidoSerializer
from datetime import date

from .models import Producto  # <--- agregar esto
from .serializers import ProductoSerializer  # <--- agregar esto

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        cantidad = serializer.validated_data.get('cantidad', 0)
        precio_unitario = serializer.validated_data.get('precio_unitario', 0)
        total = cantidad * precio_unitario

        fecha = serializer.validated_data.get('fecha', date.today())
        estado = serializer.validated_data.get('estado', 'pendiente')

        serializer.save(total=total, fecha=fecha, estado=estado)

    def perform_update(self, serializer):
        cantidad = serializer.validated_data.get('cantidad', 0)
        precio_unitario = serializer.validated_data.get('precio_unitario', 0)
        total = cantidad * precio_unitario

        instance = self.get_object()
        fecha = serializer.validated_data.get('fecha', instance.fecha)
        estado = serializer.validated_data.get('estado', instance.estado)

        serializer.save(total=total, fecha=fecha, estado=estado)

# NUEVO:
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
