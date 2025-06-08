from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_page, name='payment_page'),
    path('create/', views.create_payment, name='create_payment'), 
    path('execute/', views.execute_payment, name='execute_payment'),
    path('cancel/', views.cancel_payment, name='cancel_payment'), 
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path('create-payment/', views.create_payment, name='create_payment'),
]
