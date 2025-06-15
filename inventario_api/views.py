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

    try:
        data = request.data
        print("🔥 DATA:", data)

        producto_id = int(data.get("producto_id"))
        cantidad = int(data.get("cantidad"))
        print(f"🧪 producto_id: {producto_id} cantidad: {cantidad}")
    except Exception as e:
        return Response({"error": f"Error al procesar datos: {str(e)}"}, status=400)

    try:
        producto = Producto.objects.get(pk=producto_id)
    except Producto.DoesNotExist:
        return Response({"error": "Producto no encontrado."}, status=404)

    if producto.stock_disponible < cantidad:
        return Response({"error": "Stock insuficiente."}, status=400)

    producto.stock_disponible -= cantidad
    producto.save()

    return Response({
        "message": "Stock actualizado correctamente.",
        "producto_id": producto.id,
        "nuevo_stock": producto.stock_disponible
    }, status=200)

