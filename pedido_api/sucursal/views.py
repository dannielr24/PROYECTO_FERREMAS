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
