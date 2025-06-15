import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse
import requests  # Para llamadas a la API de inventario

# Configuración de PayPal
paypalrestsdk.configure({
    "mode": "sandbox",
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
    carrito = request.session.get("carrito", {})
    if not carrito:
        return HttpResponse("El carrito está vacío.")

    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    items = [{
        "name": item['nombre'],
        "sku": str(producto_id),
        "price": f"{item['precio']:.2f}",
        "currency": "USD",
        "quantity": item['cantidad']
    } for producto_id, item in carrito.items()]

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
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

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
        return HttpResponse("Error: no se encontró la URL de aprobación de PayPal.")
    else:
        return HttpResponse("Error al crear el pago: " + payment.error['message'])

@require_GET
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    if not payment_id or not payer_id:
        return HttpResponse("Faltan parámetros de pago.")

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        carrito = request.session.get("carrito", {})

        for producto_id, item in carrito.items():
            print(f"Descontando stock del producto {producto_id} en {item['cantidad']}")
            try:
                res = requests.post("http://localhost:8000/api/inventario/descontar-stock/", json={
                    "producto_id": int(producto_id),
                    "cantidad": item["cantidad"]
                })
                print(f"Respuesta stock: {res.status_code} - {res.text}")
            except Exception as e:
                print(f"❌ Error al llamar a la API: {e}")

        request.session["carrito"] = {}
        return render(request, "payment/success.html")
    else:
        return render(request, "payment/error.html", {"error": payment.error})

@require_GET
def cancel_payment(request):
    return render(request, "cancel.html")

def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())
    return render(request, "carrito.html", {"carrito": carrito, "total": total})
