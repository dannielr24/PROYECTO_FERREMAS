from rest_framework import serializers
from inventario_api.models import Pedido, Producto
from inventario_api.serializers import ProductoSerializer

class PedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)  # Muestra los datos del producto al hacer GET
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),  # Permite enviar solo el ID del producto
        write_only=True,
        source='producto'
    )

    class Meta:
        model = Pedido
        fields = [
            'id',
            'producto',      # Solo lectura: muestra datos anidados
            'producto_id',   # Solo escritura: para crear o actualizar con el ID
            'cantidad',
            'fecha',
            'nombre_comprador',
            'email_comprador',
            'telefono_comprador'
        ]
