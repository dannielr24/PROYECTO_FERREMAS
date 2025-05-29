from django.contrib import admin
from .models import Sucursal, InventarioSucursal, TransferenciaProducto

admin.site.register(Sucursal)
admin.site.register(InventarioSucursal)
admin.site.register(TransferenciaProducto)
