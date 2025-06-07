from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include('tienda_web.urls')),
    path('admin/', admin.site.urls),
    path('api/pedidos/', include(router.urls)),
    path('api/inventario/', include('inventario_api.urls')),
    path('api/sucursal/', include('sucursal.urls')),
    path('payment/', include('pagos_api.urls')),
]
