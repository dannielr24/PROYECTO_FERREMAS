from django.urls import path
from . import views

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
]

