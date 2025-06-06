from django.shortcuts import redirect
from django.http import HttpResponse
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions

# Configuración manual para entorno de pruebas
commerce_code = '597055555532'
api_key = '597055555532'
integration_type = IntegrationType.TEST

options = WebpayOptions(commerce_code, api_key, integration_type)
transaction = Transaction(options)

def iniciar_pago(request):
    buy_order = "orden12345"
    session_id = "sesion12345"
    amount = 10000
    return_url = request.build_absolute_uri('/pagos/confirmacion/')

    try:
        response = transaction.create(buy_order, session_id, amount, return_url)
        token = response.token
        url = response.url
        return redirect(f"{url}?token_ws={token}")
    except Exception as e:
        return HttpResponse(f"❌ Error al iniciar la transacción: {e}")

def confirmacion_pago(request):
    token_ws = request.GET.get('token_ws') or request.POST.get('token_ws')
    if not token_ws:
        return HttpResponse("❌ Error: no se recibió token_ws.")

    try:
        result = transaction.commit(token_ws)
    except Exception as e:
        return HttpResponse(f"❌ Error al confirmar la transacción: {e}")

    if result.status == "AUTHORIZED":
        mensaje = (
            f"✅ Pago autorizado!<br>"
            f"🧾 Orden: {result.buy_order}<br>"
            f"💵 Monto: {result.amount}<br>"
            f"💳 Tarjeta: {result.card_detail.card_number}"
        )
    else:
        mensaje = f"❌ Pago no autorizado. Estado: {result.status}"

    return HttpResponse(mensaje)
