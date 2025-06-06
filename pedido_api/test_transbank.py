from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType

commerce_code = "597055555532"
api_key = "0800200001643993"
integration_type = IntegrationType.TEST

options = WebpayOptions(commerce_code, api_key, integration_type)
transaction = Transaction(options)

try:
    response = transaction.create(
        "order_test_001",
        "session_test_001",
        1000,
        "http://127.0.0.1:8000/pagos/confirmacion/"  # URL válida en tu entorno
    )
    print("✅ Token:", response.token)
    print("🌐 URL:", response.url)
except Exception as e:
    print("❌ Error al crear la transacción:", e)
