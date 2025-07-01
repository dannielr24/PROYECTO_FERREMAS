from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from control_api.models import Pedido
from control_api.serializers import PedidoSerializer
from datetime import date

from .models import Producto
from .serializers import ProductoSerializer

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


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


@api_view(['POST'])
def descontar_stock(request):
    print("🔥 MÉTODO:", request.method)
    print("🔥 HEADERS:", request.headers)
    print("🔥 BODY CRUDO:", request.body)
    print("🔥 DATA:", request.data)

    producto_id = request.data.get("producto_id")
    cantidad = request.data.get("cantidad")

    print("🧪 producto_id:", producto_id, "cantidad:", cantidad)

    # Validación de producto_id
    if not producto_id:
        return Response({"error": "ID de producto es requerido"}, status=400)

    # Validación y conversión de cantidad
    try:
        cantidad = int(cantidad)
    except (ValueError, TypeError):
        return Response({"error": "Error al procesar datos"}, status=400)

    if cantidad == 0:
        return Response({"error": "Cantidad debe ser mayor que cero"}, status=400)

    if cantidad < 0:
        return Response({"error": "Cantidad no puede ser negativa"}, status=400)

    try:
        producto = Producto.objects.get(pk=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=404)

    if producto.stock_disponible < cantidad:
        return Response({"error": "Stock insuficiente"}, status=400)

    # Descontar stock
    producto.stock_disponible -= cantidad
    producto.save()

    return Response({"mensaje": "Stock descontado correctamente", "nuevo_stock": producto.stock_disponible}, status=200)
