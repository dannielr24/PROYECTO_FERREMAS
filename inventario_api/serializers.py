from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'marca', 'nombre', 'precio', 'descripcion', 'categoria', 'stock_disponible', 'imagen']
