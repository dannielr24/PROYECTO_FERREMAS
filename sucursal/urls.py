from rest_framework.routers import DefaultRouter
from .views import SucursalViewSet, InventarioSucursalViewSet, TransferenciaProductoViewSet

router = DefaultRouter()
router.register(r'sucursales', SucursalViewSet)
router.register(r'inventario-sucursal', InventarioSucursalViewSet)
router.register(r'transferencias', TransferenciaProductoViewSet)

urlpatterns = router.urls
