from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('pago-confirmado/', views.pago_confirmado, name='pago_confirmado'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    # NUEVAS:
    path('sucursales/', views.sucursales, name='sucursales'),
    path('transferencias/', views.transferencias, name='transferencias'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path("limpiar-carrito/", views.limpiar_carrito, name="limpiar_carrito"),
    path('sucursal/<int:sucursal_id>/productos/', views.productos_sucursal, name='productos_sucursal'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('carrito/aumentar/<int:producto_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('carrito/disminuir/<int:producto_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('boleta/<int:boleta_id>/', views.ver_boleta, name='ver_boleta'),
    path('historial-compras/', views.historial_compras, name='historial_compras'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

