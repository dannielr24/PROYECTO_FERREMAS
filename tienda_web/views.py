from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import requests

# URL base de tus APIs
API_PRODUCTOS_URL = 'http://localhost:8000/api/inventario/productos/'
API_SUCURSALES_URL = 'http://localhost:8000/api/sucursal/sucursales/'
API_TRANSFERENCIAS_URL = 'http://localhost:8000/api/sucursal/transferencias/'
API_PEDIDOS_URL = 'http://localhost:8000/api/pedidos/'

def catalogo(request):
    response = requests.get(API_PRODUCTOS_URL)
    productos = response.json() if response.status_code == 200 else []
    return render(request, 'productos.html', {'productos': productos})

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    response = requests.get(f"{API_PRODUCTOS_URL}{producto_id}/")
    if response.status_code != 200:
        return redirect("catalogo")

    producto = response.json()
    producto_data = {
        "nombre": producto["nombre"],
        "precio": float(producto["precio"]),
        "cantidad": 1,
        "imagen": producto["imagen"] if "imagen" in producto and producto["imagen"] else ""
    }

    if str(producto_id) in carrito:
        carrito[str(producto_id)]["cantidad"] += 1
    else:
        carrito[str(producto_id)] = producto_data

    request.session["carrito"] = carrito
    return redirect("carrito")

def carrito(request):
    carrito = request.session.get("carrito", {})
    total = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values())
    return render(request, 'carrito.html', {"carrito": carrito, "total": total})

def checkout(request):
    carrito = request.session.get("carrito", {})
    total = sum(item["precio"] * item["cantidad"] for item in carrito.values())
    return render(request, 'checkout.html', {"carrito": carrito, "total": total})

def pago_confirmado(request):
    # request.session["carrito"] = {}
    return render(request, 'pago_confirmado.html')

# NUEVAS VIEWS

def sucursales(request):
    response = requests.get(API_SUCURSALES_URL)
    sucursales = response.json() if response.status_code == 200 else []
    return render(request, 'sucursales.html', {'sucursales': sucursales})

def transferencias(request):
    response = requests.get(API_TRANSFERENCIAS_URL)
    transferencias = response.json() if response.status_code == 200 else []

    # Obtener productos
    productos_response = requests.get(API_PRODUCTOS_URL)
    productos = productos_response.json() if productos_response.status_code == 200 else []

    # Obtener sucursales
    sucursales_response = requests.get(API_SUCURSALES_URL)
    sucursales = sucursales_response.json() if sucursales_response.status_code == 200 else []

    if request.method == "POST":
        data = {
            "producto": request.POST.get("producto_id"),
            "sucursal_origen": request.POST.get("sucursal_origen"),
            "sucursal_destino": request.POST.get("sucursal_destino"),
            "cantidad": request.POST.get("cantidad"),
        }
        transfer_response = requests.post(API_TRANSFERENCIAS_URL, json=data)
        if transfer_response.status_code in [200, 201]:
            return redirect("transferencias")

    return render(request, 'transferencias.html', {
        'transferencias': transferencias,
        'productos': productos,
        'sucursales': sucursales
    })

@staff_member_required(login_url='/admin/login/')
def admin_page(request):
    return render(request, 'admin_page.html')

def limpiar_carrito(request):
    request.session["carrito"] = {}
    return redirect("carrito")

def productos_sucursal(request, sucursal_id):
    # Obtener info de la sucursal
    sucursal_response = requests.get(f"{API_SUCURSALES_URL}{sucursal_id}/")
    if sucursal_response.status_code != 200:
        return redirect("sucursales")

    sucursal = sucursal_response.json()

    # Obtener inventario de sucursal
    inventario_response = requests.get("http://localhost:8000/api/sucursal/inventario-sucursal/")
    inventario = inventario_response.json() if inventario_response.status_code == 200 else []

    # Filtrar inventario para esta sucursal (más simple en tu caso)
    inventario_filtrado = [item for item in inventario if item["sucursal"] == sucursal_id]

    # Obtener productos
    productos_response = requests.get(API_PRODUCTOS_URL)
    productos = productos_response.json() if productos_response.status_code == 200 else []

    # Construir lista de productos con stock en esta sucursal
    productos_en_sucursal = []
    for item in inventario_filtrado:
        # Aquí item["producto"] es un int (perfecto)
        producto = next((p for p in productos if p["id"] == item["producto"]), None)
        if producto:
            productos_en_sucursal.append({
                "nombre": producto["nombre"],
                "descripcion": producto["descripcion"],
                "precio": producto["precio"],
                "imagen": producto.get("imagen", ""),
                "stock": item["stock"]
            })

    return render(request, "productos_sucursal.html", {
        "sucursal": sucursal,
        "productos": productos_en_sucursal
    })
    
    # LOGIN para clientes
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("catalogo")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("catalogo")

# REGISTRO para clientes
def registro(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
        else:
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, "Usuario creado. Ahora puedes iniciar sesión.")
            return redirect("login")
    return render(request, "registro.html")
