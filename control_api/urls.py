from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    # otras rutas
    path('admin/', admin.site.urls),
    path('api/pedidos/', include('pedido_api.urls')),
    path('api/inventario/', include('inventario_api.urls')),
    path('api/sucursal/', include('sucursal.urls')),
    path('', include('tienda_web.urls')),
]
