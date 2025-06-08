import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse  # ✅ Para generar URLs dinámicas


# Configuración del SDK de PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambiar a "live" en producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})


@require_GET
def payment_page(request):
    carrito = request.session.get("carrito", {})
    total = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values())
    return render(request, 'payment.html', {"carrito": carrito, "total": total})


@require_POST
def create_payment(request):
    """Vista para crear un pago usando los datos del carrito de compras"""

    # Obtener carrito de la sesión
    carrito = request.session.get("carrito", {})
    if not carrito:
        return HttpResponse("El carrito está vacío.")

    # Calcular total
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    # Crear lista de productos para PayPal
    items = [{
        "name": item['nombre'],
        "sku": str(producto_id),
        "price": f"{item['precio']:.2f}",
        "currency": "USD",
        "quantity": item['cantidad']
    } for producto_id, item in carrito.items()]

    # ✅ Crear el pago con URLs generadas dinámicamente
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('cancel_payment'))
        },
        "transactions": [{
            "item_list": {"items": items},
            "amount": {
                "total": f"{total:.2f}",
                "currency": "USD"
            },
            "description": "Pago del carrito de compras"
        }]
    })

    # Procesar el pago
    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
        return HttpResponse("Error: no se encontró la URL de aprobación de PayPal.")
    else:
        return HttpResponse("Error al crear el pago: " + payment.error['message'])


@require_GET
def execute_payment(request):
    """Vista para completar el pago después de la aprobación del usuario"""
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        return HttpResponse("Faltan parámetros de pago.")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Vaciar el carrito
        request.session["carrito"] = {}
        return render(request, "payment/success.html")
    else:
        return render(request, "payment/error.html", {"error": payment.error})


@require_GET
def cancel_payment(request):
    """Vista para cuando el usuario cancela el pago"""
    return render(request, "cancel.html")


def ver_carrito(request):
    """Vista para mostrar los productos del carrito"""
    carrito = request.session.get("carrito", {})
    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())
    return render(request, "carrito.html", {"carrito": carrito, "total": total})
