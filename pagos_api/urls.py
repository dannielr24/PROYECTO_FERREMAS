from django.urls import path
from . import views

urlpatterns = [
    path('iniciar/',      views.iniciar_pago,      name='iniciar_pago'),
    path('confirmacion/', views.confirmacion_pago, name='confirmacion_pago'),
]
