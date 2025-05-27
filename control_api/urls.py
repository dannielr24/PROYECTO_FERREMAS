from django.urls import path, include

urlpatterns = [
    # otras rutas
    path('api/', include('pedido_api.urls')),
]
