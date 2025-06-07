from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, ProductoViewSet  # <--- agregar ProductoViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'productos', ProductoViewSet, basename='producto')  # <--- agregar esto

urlpatterns = [
    path('', include(router.urls)),
]
