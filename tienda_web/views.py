from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Boleta, DetalleBoleta
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
    total = 0

    # Generamos lista de items con subtotal incluido
    for item in carrito.values():
        item['subtotal'] = item['precio'] * item['cantidad']
        total += item['subtotal']

    return render(request, 'carrito.html', {"carrito": carrito, "total": total})

def checkout(request):
    carrito = request.session.get("carrito", {})
    total_clp = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values())

    # Obtener API mindicador
    indicadores = requests.get("https://mindicador.cl/api").json()

    dolar_value = indicadores["dolar"]["valor"]
    euro_value = indicadores["euro"]["valor"]
    uf_value = indicadores["uf"]["valor"]
    utm_value = indicadores["utm"]["valor"]

    # Convertir total
    total_usd = round(total_clp / dolar_value, 2)
    total_eur = round(total_clp / euro_value, 2)
    total_uf = round(total_clp / uf_value, 2)
    total_utm = round(total_clp / utm_value, 2)

    return render(request, 'checkout.html', {
        "carrito": carrito,
        "total_clp": total_clp,
        "total_usd": total_usd,
        "total_eur": total_eur,
        "total_uf": total_uf,
        "total_utm": total_utm,
        "dolar_value": dolar_value,
        "euro_value": euro_value,
        "uf_value": uf_value,
        "utm_value": utm_value
    })

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

def get_dolar_value():
    try:
        response = requests.get("https://mindicador.cl/api/dolar")
        response.raise_for_status()  # Lanza excepción si la respuesta no es 200 OK
        data = response.json()
        dolar_value = data["serie"][0]["valor"]  # El valor más reciente
        return dolar_value
    except Exception as e:
        print("Error obteniendo el valor del dólar:", e)
        return 900  # Valor de respaldo por si la API falla
    
def get_euro_value():
    try:
        response = requests.get("https://mindicador.cl/api/euro")
        data = response.json()
        return data["serie"][0]["valor"]
    except Exception:
        return 1100  # Valor por defecto si falla
    
def aumentar_cantidad(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        carrito[producto_id_str]["cantidad"] += 1

    request.session["carrito"] = carrito
    return redirect("carrito")

def disminuir_cantidad(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        if carrito[producto_id_str]["cantidad"] > 1:
            carrito[producto_id_str]["cantidad"] -= 1
        else:
            # Si cantidad es 1 y se disminuye → eliminar producto
            del carrito[producto_id_str]

    request.session["carrito"] = carrito
    return redirect("carrito")

def eliminar_producto(request, producto_id):
    carrito = request.session.get("carrito", {})
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        del carrito[producto_id_str]

    request.session["carrito"] = carrito
    return redirect("carrito")

def generar_boleta(request):
    if not request.user.is_authenticated:
        return redirect("login")

    carrito = request.session.get("carrito", {})
    if not carrito:
        messages.error(request, "Tu carrito está vacío.")
        return redirect("carrito")

    total = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values())
    boleta = Boleta.objects.create(usuario=request.user, total=total)

    for producto_id, item in carrito.items():
        DetalleBoleta.objects.create(
            boleta=boleta,
            producto_id=int(producto_id),
            cantidad=item["cantidad"],
            precio_unitario=item["precio"]
        )

    request.session["carrito"] = {}
    return render(request, "boleta_generada.html", {"boleta": boleta})


def historial_compras(request):
    if not request.user.is_authenticated:
        return redirect("login")

    boletas = Boleta.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, "historial_compras.html", {"boletas": boletas})

