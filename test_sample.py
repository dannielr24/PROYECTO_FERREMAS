import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_crear_pedido():
    client = APIClient()

    data = {
        "producto": "Producto Test",
        "cantidad": 3,
        "cliente": "Cliente Test",
        "direccion": "Calle Falsa 123",
        "precio_unitario": "100.00",
    }

    response = client.post('/api/pedidos/', data, format='json')

    if response.status_code != 201:
        print("Error detalle:", response.data)

    assert response.status_code == 201
    assert float(response.data['total']) == 300.00
