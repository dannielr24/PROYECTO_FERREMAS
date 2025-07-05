from rest_framework import serializers
from pedido_api.models import Pedido
from inventario_api.models import Producto
from inventario_api.serializers import ProductoSerializer

class PedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        write_only=True,
        source='producto'
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            'id',
            'producto',
            'producto_id',
            'cantidad',
            'fecha',
            'nombre_comprador',
            'email_comprador',
            'telefono_comprador',
            'total'
        ]
        read_only_fields = ['fecha', 'total']

    def get_total(self, obj):
        return obj.producto.precio * obj.cantidad

    def validate(self, data):
        if data['cantidad'] <= 0:
            raise serializers.ValidationError({"cantidad": "La cantidad debe ser mayor a cero"})
        
        producto = data.get('producto') or self.instance.producto
        if data['cantidad'] > producto.stock_disponible:
            raise serializers.ValidationError(
                {"cantidad": "No hay suficiente stock disponible"}
            )
        return data