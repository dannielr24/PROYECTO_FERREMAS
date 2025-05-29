from rest_framework import serializers
from .models import Sucursal, InventarioSucursal, TransferenciaProducto

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class InventarioSucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventarioSucursal
        fields = '__all__'

class TransferenciaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferenciaProducto
        fields = '__all__'

    def create(self, validated_data):
        transferencia = TransferenciaProducto(**validated_data)
        transferencia.save()  # Aquí se ejecuta el método save() con la lógica de stock
        return transferencia
