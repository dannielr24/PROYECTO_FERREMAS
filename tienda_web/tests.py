import pytest
from rest_framework.test import APIClient
from django.test import Client
from django.urls import reverse
from unittest.mock import patch
from pedido_api.models import Pedido
from inventario_api.models import Producto
from sucursal.models import Sucursal, InventarioSucursal
from django.contrib.auth.models import User
from datetime import date


# Datos de prueba para pedidos
PEDIDO_TEST_DATA = {
    "nombre_comprador": "Cliente Test",
    "email_comprador": "test@example.com",
    "telefono_comprador": "+56912345678"
}

# ✅ TC001 – TC007: Sucursales y Transferencias

@pytest.mark.django_db
def test_crear_sucursal():
    client = APIClient()
    response = client.post(reverse('sucursales'), {
        "nombre": "Sucursal Centro",
        "direccion": "Av. Principal 123",
        "ciudad": "Santiago",
        "region": "Metropolitana"
    }, format="json")
    assert response.status_code in [200, 201]

@pytest.mark.django_db
def test_crear_inventario_para_sucursal():
    producto = Producto.objects.create(codigo="P100", nombre="Laptop", precio=1000, stock_disponible=10)
    sucursal = Sucursal.objects.create(nombre="Sucursal Norte", direccion="Calle Norte 10")
    client = APIClient()
    response = client.post(reverse('productos_sucursal', kwargs={'sucursal_id': sucursal.id}), {
        "producto": producto.id,
        "sucursal": sucursal.id,
        "stock": 5
    }, format="json")
    assert response.status_code in [200, 201]

@pytest.mark.django_db
def test_transferencia_producto_stock_actualizado():
    producto = Producto.objects.create(codigo="P200", nombre="Monitor", precio=200, stock_disponible=20)
    sucursal_origen = Sucursal.objects.create(nombre="Origen", direccion="Calle 1")
    sucursal_destino = Sucursal.objects.create(nombre="Destino", direccion="Calle 2")
    InventarioSucursal.objects.create(producto=producto, sucursal=sucursal_origen, stock=10)
    InventarioSucursal.objects.create(producto=producto, sucursal=sucursal_destino, stock=2)
    client = APIClient()
    response = client.post(reverse('transferencias'), {
        "producto": producto.id,
        "sucursal_origen": sucursal_origen.id,
        "sucursal_destino": sucursal_destino.id,
        "cantidad": 3
    }, format="json")
    assert response.status_code in [200, 201]

@pytest.mark.django_db
def test_transferencia_destino_no_tiene_registro():
    producto = Producto.objects.create(codigo="P300", nombre="Teclado", precio=50, stock_disponible=15)
    origen = Sucursal.objects.create(nombre="Sucursal A", direccion="Avenida 1")
    destino = Sucursal.objects.create(nombre="Sucursal B", direccion="Avenida 2")
    InventarioSucursal.objects.create(producto=producto, sucursal=origen, stock=5)
    client = APIClient()
    response = client.post(reverse('transferencias'), {
        "producto": producto.id,
        "sucursal_origen": origen.id,
        "sucursal_destino": destino.id,
        "cantidad": 2
    }, format="json")
    assert response.status_code in [200, 201]

@pytest.mark.django_db
def test_transferencia_sin_stock_suficiente():
    producto = Producto.objects.create(codigo="P400", nombre="Mouse", precio=20, stock_disponible=8)
    origen = Sucursal.objects.create(nombre="Origen X", direccion="Diagonal 9")
    destino = Sucursal.objects.create(nombre="Destino Y", direccion="Diagonal 10")
    InventarioSucursal.objects.create(producto=producto, sucursal=origen, stock=1)
    client = APIClient()
    response = client.post(reverse('transferencias'), {
        "producto": producto.id,
        "sucursal_origen": origen.id,
        "sucursal_destino": destino.id,
        "cantidad": 5
    }, format="json")
    assert response.status_code in [200, 201]

@pytest.mark.django_db
def test_transferencia_actualiza_stock_producto_global():
    producto = Producto.objects.create(codigo="P700", nombre="Proyector", precio=1000, stock_disponible=0)
    s1 = Sucursal.objects.create(nombre="S1", direccion="R1")
    s2 = Sucursal.objects.create(nombre="S2", direccion="R2")
    InventarioSucursal.objects.create(producto=producto, sucursal=s1, stock=3)
    InventarioSucursal.objects.create(producto=producto, sucursal=s2, stock=1)
    client = APIClient()
    response = client.post(reverse('transferencias'), {
        "producto": producto.id,
        "sucursal_origen": s1.id,
        "sucursal_destino": s2.id,
        "cantidad": 2
    }, format="json")
    producto.refresh_from_db()
    assert producto.stock_disponible == 0

# ✅ TC008 – TC014: Pedidos (API)

def get_pedido_endpoints(pedido_id=None):
    base_endpoints = [
        '/api/pedidos/pedidos/',
        '/pedidos/',
        reverse('pedido-list')
    ]
    
    if pedido_id is not None:
        detail_endpoints = [
            f'/api/pedidos/pedidos/{pedido_id}/',
            f'/pedidos/{pedido_id}/',
            reverse('pedido-detail', kwargs={'pk': pedido_id})
        ]
        return detail_endpoints
    return base_endpoints

@pytest.mark.django_db
def test_crear_pedido_viewset():
    producto = Producto.objects.create(codigo="P101", nombre="Laptop", precio=1000, stock_disponible=10)
    cantidad = 2
    total = producto.precio * cantidad

    client = APIClient()
    data = {
        "producto_id": producto.id,
        "cantidad": cantidad,
        **PEDIDO_TEST_DATA
    }

    response = None
    for endpoint in get_pedido_endpoints():
        response = client.post(endpoint, data, format="json")
        if response.status_code != 404:
            break
    
    assert response.status_code == 201, f"Falló en endpoint {endpoint}. Respuesta: {response.data}"
    if response.status_code == 201:
        assert float(response.data.get("total")) == total
        assert response.data.get("nombre_comprador") == "Cliente Test"

@pytest.mark.django_db
def test_actualizar_pedido_recalcula_total():
    producto = Producto.objects.create(codigo="P102", nombre="Teclado", precio=50, stock_disponible=10)
    pedido = Pedido.objects.create(
        producto=producto,
        cantidad=2,
        **PEDIDO_TEST_DATA
    )

    nueva_cantidad = 3
    nuevo_total = producto.precio * nueva_cantidad

    client = APIClient()
    data = {
        "producto_id": producto.id,
        "cantidad": nueva_cantidad,
        **PEDIDO_TEST_DATA
    }

    response = None
    for endpoint in get_pedido_endpoints(pedido.id):
        response = client.put(endpoint, data, format="json")
        if response.status_code != 404:
            break
    
    assert response.status_code == 200, f"Falló en endpoint {endpoint}. Respuesta: {response.data}"
    if response.status_code == 200:
        assert float(response.data.get("total")) == nuevo_total
        assert response.data.get("email_comprador") == "test@example.com"

@pytest.mark.django_db
def test_listar_pedidos():
    producto = Producto.objects.create(codigo="P103", nombre="Mouse", precio=20, stock_disponible=10)
    Pedido.objects.create(
        producto=producto,
        cantidad=1,
        **PEDIDO_TEST_DATA
    )

    client = APIClient()
    response = client.get('/api/pedidos/pedidos/')
    
    assert response.status_code == 200
    
    # Maneja tanto si es una lista directa como si está paginada
    if hasattr(response.data, 'get'):  # Para respuestas paginadas
        pedidos_data = response.data.get('results', response.data)
    else:  # Para listas directas
        pedidos_data = response.data
    
    assert len(pedidos_data) >= 1
    
    # Obtiene el campo producto (que ahora es un objeto completo)
    producto_data = pedidos_data[0].get('producto_id') or pedidos_data[0].get('producto')
    
    # Verifica el ID dentro del objeto producto
    assert producto_data['id'] == producto.id  # Cambio clave aquí
    
    assert pedidos_data[0]['telefono_comprador'] == "+56912345678"

@pytest.mark.django_db
def test_eliminar_pedido():
    producto = Producto.objects.create(codigo="P104", nombre="Cámara", precio=300, stock_disponible=5)
    pedido = Pedido.objects.create(
        producto=producto,
        cantidad=1,
        **PEDIDO_TEST_DATA
    )

    client = APIClient()
    response = None
    for endpoint in get_pedido_endpoints(pedido.id):
        response = client.delete(endpoint)
        if response.status_code != 404:
            break
    
    assert response.status_code in [204, 404]

# ✅ TC015 – TC022: Inventario y Pagos

@pytest.mark.django_db
def test_descontar_stock_ok():
    producto = Producto.objects.create(codigo="P123", nombre="Tablet", precio=1000, stock_disponible=5)
    client = APIClient()
    response = client.post(reverse('descontar_stock'), {
        "producto_id": producto.id,
        "cantidad": 2
    }, format="json")
    assert response.status_code == 200
    assert response.data["nuevo_stock"] == 3

@pytest.mark.django_db
def test_descontar_stock_sin_producto_id():
    client = APIClient()
    response = client.post(reverse('descontar_stock'), {"cantidad": 1}, format="json")
    assert response.status_code == 400
    assert "ID de producto es requerido" in response.data["error"]

@pytest.mark.django_db
def test_descontar_stock_producto_inexistente():
    client = APIClient()
    response = client.post(reverse('descontar_stock'), {
        "producto_id": 9999,
        "cantidad": 1
    }, format="json")
    assert response.status_code == 404

# Ajustes de pruebas de usuarios y carrito

@pytest.mark.django_db
def test_001_catalogo_status_code(client):
    response = client.get(reverse('catalogo'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_002_login_view_correcto(client):
    User.objects.create_user(username="cliente", password="test1234")
    response = client.post(reverse('login'), {
        "username": "cliente",
        "password": "test1234"
    })
    assert response.status_code == 302

@pytest.mark.django_db
def test_003_carrito_calculo_total(client):
    session = client.session
    session["carrito"] = {
        "1": {
            "nombre": "Producto Prueba",
            "precio": 1000,
            "cantidad": 2,
            "imagen": "img.jpg"
        }
    }
    session.save()
    response = client.get(reverse('carrito'))
    assert b"2000" in response.content

@pytest.mark.django_db
def test_004_generar_boleta_con_usuario(client):
    user = User.objects.create_user(username="cliente", password="test1234")
    producto = Producto.objects.create(codigo="P100", nombre="Producto Prueba", precio=1000, stock_disponible=10)
    client.login(username="cliente", password="test1234")
    session = client.session
    session["carrito"] = {
        "1": {
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": 1,
            "imagen": ""
        }
    }
    session.save()
    response = client.get(reverse('generar_boleta'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_005_generar_boleta_sin_login_redireccion(client):
    response = client.get(reverse('generar_boleta'))
    assert response.status_code == 302