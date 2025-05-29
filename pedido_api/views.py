from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Pedido
from .serializers import PedidoSerializer
from inventario_api.models import Producto
from rest_framework import serializers


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        producto = serializer.validated_data['producto']
        cantidad = serializer.validated_data['cantidad']

        if producto.stock_disponible < cantidad:
            raise serializers.ValidationError("No hay suficiente stock disponible.")

        # Descontar stock del producto
        producto.stock_disponible -= cantidad
        producto.save()

        serializer.save()
