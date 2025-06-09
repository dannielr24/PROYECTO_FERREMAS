from django.shortcuts import render, redirect
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

    return render(request, 'transferencias.html', {'transferencias': transferencias})

def admin_page(request):
    return render(request, 'admin_page.html')

# tienda_web/views.py

def limpiar_carrito(request):
    request.session["carrito"] = {}
    return redirect("carrito")
