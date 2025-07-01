# 🛠️ PROYECTO_FERREMAS - Instrucciones de Ejecución

Este proyecto corresponde a la API backend del sistema de e-commerce **Ferremas**, desarrollado con Django y Django REST Framework. Aquí se incluye la configuración, ejecución del servidor y pruebas unitarias necesarias para validar el correcto funcionamiento.

---

## 📁 Requisitos Previos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu máquina:

- **Python 3.9 o superior**  
  Verifica con:
  ```bash
  python --version
  ```

- **Git**
  ```bash
  git --version
  ```

- **Virtualenv** (opcional pero recomendado):
  ```bash
  pip install virtualenv
  ```

---

## 📥 Clonación del Repositorio

```bash
git clone https://github.com/dannielr24/PROYECTO_FERREMAS.git
cd PROYECTO_FERREMAS
```

---

## 🧪 Creación y Activación de Entorno Virtual

### En Windows:
```bash
python -m venv env
env\Scripts\activate
```

### En Mac/Linux:
```bash
python3 -m venv env
source env/bin/activate
```

---

## 📦 Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Contenido mínimo recomendado:
```txt
Django==4.2.13
djangorestframework
pytest
pytest-django
```

---

## ⚙️ Configuración del Proyecto

1. Verifica que en `control_api/settings.py` esté correctamente configurada la base de datos (`sqlite3` por defecto).
2. Ejecuta las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. (Opcional) Crea un superusuario:
```bash
python manage.py createsuperuser
```

---

## ▶️ Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Luego visita en tu navegador:  
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## ✅ Ejecutar Pruebas Unitarias

```bash
python -m pytest tienda_web/tests.py
```

Resultado esperado:
```
============================== 10 passed in 0.69s ==============================
```

---

## 🧩 Estructura del Proyecto

```
PROYECTO_FERREMAS/
├── control_api/           # Proyecto principal de Django
├── tienda_web/            # App principal con vistas y APIs
├── inventario_api/        # API de inventario y stock
├── manage.py              # Script de administración
├── requirements.txt       # Librerías necesarias
├── pytest.ini             # Configuración para pytest-django
└── README.md              # (Este archivo)
```

---

## 🧪 Pruebas Cubiertas

- Descuento exitoso de stock
- Error por falta de `producto_id`
- Error por falta de `cantidad`
- Error por cantidad `0`
- Error por cantidad negativa
- Producto no encontrado
- Stock insuficiente
- Verificación de `nuevo_stock`
- Endpoint sin autenticación
- Validación de tipos de datos

---

## 🚀 Verificación Final para Entrega

- [x] Servidor funciona: `python manage.py runserver`
- [x] Pruebas pasan: `python -m pytest tienda_web/tests.py`
- [x] `requirements.txt` actualizado
- [x] README incluido en la raíz del proyecto
