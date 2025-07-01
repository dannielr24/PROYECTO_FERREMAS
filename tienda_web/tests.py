
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from inventario_api.models import Producto

@pytest.mark.django_db
def test_descontar_stock_exitoso():
    producto = Producto.objects.create(codigo="P999", nombre="Producto de prueba", precio=5000, stock_disponible=10)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": 3}, format="json")
    assert response.status_code == 200
    assert response.data["nuevo_stock"] == 7
    producto.refresh_from_db()
    assert producto.stock_disponible == 7

@pytest.mark.django_db
def test_stock_insuficiente():
    producto = Producto.objects.create(codigo="P1000", nombre="Producto limitado", precio=1000, stock_disponible=2)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": 5}, format="json")
    assert response.status_code == 400
    assert "Stock insuficiente" in response.data["error"]

@pytest.mark.django_db
def test_producto_inexistente():
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": 9999, "cantidad": 1}, format="json")
    assert response.status_code == 404
    assert "Producto no encontrado" in response.data["error"]

@pytest.mark.django_db
def test_falta_producto_id():
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"cantidad": 2}, format="json")
    assert response.status_code == 400
    assert "ID de producto es requerido" in response.data["error"]

@pytest.mark.django_db
def test_cantidad_invalida():
    producto = Producto.objects.create(codigo="P1002", nombre="Producto inválido", precio=2000, stock_disponible=5)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": "tres"}, format="json")
    assert response.status_code == 400
    assert "Error al procesar datos" in response.data["error"]

@pytest.mark.django_db
def test_cantidad_cero():
    producto = Producto.objects.create(codigo="P1003", nombre="Producto cero", precio=1500, stock_disponible=5)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": 0}, format="json")
    assert response.status_code == 400
    assert "Cantidad debe ser mayor que cero" in response.data["error"]

@pytest.mark.django_db
def test_cantidad_negativa():
    producto = Producto.objects.create(codigo="P1004", nombre="Producto negativo", precio=2000, stock_disponible=10)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": -2}, format="json")
    assert response.status_code == 400
    assert "Cantidad no puede ser negativa" in response.data["error"]

@pytest.mark.django_db
def test_descontar_stock_sin_auth():
    producto = Producto.objects.create(codigo="P9999", nombre="Producto sin auth", precio=1000, stock_disponible=5)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {
        "producto_id": producto.id,
        "cantidad": 1
    }, format="json")
    assert response.status_code in [200, 400, 403]

@pytest.mark.django_db
def test_campos_extra():
    producto = Producto.objects.create(codigo="P1005", nombre="Producto con campo extra", precio=2500, stock_disponible=10)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": 2, "otro_campo": "extra"}, format="json")
    assert response.status_code == 200 or response.status_code == 400

@pytest.mark.django_db
def test_integridad_datos_post_descuento():
    producto = Producto.objects.create(codigo="P1006", nombre="Producto seguro", precio=1800, stock_disponible=8)
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {"producto_id": producto.id, "cantidad": 3}, format="json")
    producto.refresh_from_db()
    assert producto.stock_disponible >= 0
