import pytest
from rest_framework.test import APIClient
from rest_framework import status
from inventario_api.models import Producto

@pytest.mark.django_db
def test_descontar_stock_exitoso():
    producto = Producto.objects.create(
        codigo="P999",
        nombre="Producto de prueba",
        precio=5000,
        stock_disponible=10
    )

    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {
        "producto_id": producto.id,
        "cantidad": 3
    }, format="json")

    assert response.status_code == 200
    assert response.data["nuevo_stock"] == 7
    producto.refresh_from_db()
    assert producto.stock_disponible == 7

@pytest.mark.django_db
def test_stock_insuficiente():
    producto = Producto.objects.create(
        codigo="P1000",
        nombre="Producto limitado",
        precio=1000,
        stock_disponible=2
    )

    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {
        "producto_id": producto.id,
        "cantidad": 5  # más del stock
    }, format="json")

    assert response.status_code == 400
    assert "Stock insuficiente" in response.data["error"]

@pytest.mark.django_db
def test_producto_inexistente():
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {
        "producto_id": 9999,  # ID que no existe
        "cantidad": 1
    }, format="json")

    assert response.status_code == 404
    assert "Producto no encontrado" in response.data["error"]

@pytest.mark.django_db
def test_falta_producto_id():
    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {
        "cantidad": 2
    }, format="json")

    assert response.status_code == 400
    assert "Error al procesar datos" in response.data["error"]

@pytest.mark.django_db
def test_cantidad_invalida():
    producto = Producto.objects.create(
        codigo="P1002",
        nombre="Producto inválido",
        precio=2000,
        stock_disponible=5
    )

    client = APIClient()
    response = client.post("/api/inventario/descontar-stock/", {
        "producto_id": producto.id,
        "cantidad": "tres"  # dato inválido
    }, format="json")

    assert response.status_code == 400
    assert "Error al procesar datos" in response.data["error"]
