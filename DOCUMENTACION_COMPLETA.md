# 📦 AMAZONCITO - Documentación Completa del Sistema

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Cómo Iniciar el Servidor](#cómo-iniciar-el-servidor)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Explicación de Archivos](#explicación-de-archivos)
6. [Estructuras de Datos Utilizadas](#estructuras-de-datos-utilizadas)
7. [Flujo Completo del Sistema](#flujo-completo-del-sistema)
8. [Base de Datos](#base-de-datos)

---

## Descripción General

**Amazoncito** es una plataforma de entrega de paquetes tipo e-commerce construida en **Django** (Python). El sistema permite:

- **Clientes**: Seleccionar productos, agregar al carrito, crear órdenes y recibir estimaciones de entrega
- **Administradores**: Gestionar órdenes, ver rutas de entrega optimizadas, cancelar pedidos
- **Algoritmo Dijkstra**: Calcula la ruta más corta entre ciudades para estimar tiempos de entrega

El proyecto implementa varias **estructuras de datos fundamentales** de la computación en situaciones reales:
- **Listas enlazadas** (LinkedList)
- **Pilas** (Stack)
- **Colas** (Queue)
- **Tablas Hash** (HashTable)
- **Grafos** (Graph) con algoritmo Dijkstra

---

## Requisitos Previos

```bash
# Sistema Operativo: Windows/Linux/Mac
# Python: 3.13+
# Django: 5.2.6

# Verificar versiones instaladas:
python --version
pip --version
```

### Dependencias Principales

```
Django==5.2.6
asgiref==3.8.1
sqlparse==0.5.0
```

---

## Cómo Iniciar el Servidor

### Paso 1: Navegar a la carpeta del proyecto

```powershell
cd "C:\amazoncito"
```

### Paso 2: Activar el entorno virtual

```powershell
# En Windows PowerShell
.\venv\Scripts\Activate.ps1

# En terminal CMD
venv\Scripts\activate.bat
```

### Paso 3: Aplicar migraciones (primera vez)

```powershell
python manage.py migrate
```

### Paso 4: Crear datos iniciales (primera vez)

```powershell
# Crear admin
python manage.py runserver &
# Luego en el navegador: http://127.0.0.1:8000/api/init-admin/
# Luego: http://127.0.0.1:8000/api/init-data/

# O crear un superusuario
python manage.py createsuperuser
```

### Paso 5: Inicializar rutas y ciudades

```powershell
python initialize_routes.py
```

### Paso 6: Iniciar el servidor

```powershell
python manage.py runserver
```

**Salida esperada:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Acceso a la aplicación

- **Cliente**: http://127.0.0.1:8000/ (login con usuario cliente)
- **Admin**: http://127.0.0.1:8000/ (login con usuario admin)
- **Panel Admin Django**: http://127.0.0.1:8000/django-admin/

### Credenciales de Prueba

```
Usuario Admin:
  username: admin
  password: Amazoncito123

O crear nuevo cliente en registro
```

---

## Estructura del Proyecto

```
amazoncito/
├── amazoncito/                    # Carpeta principal de configuración
│   ├── __init__.py
│   ├── asgi.py                   # Configuración ASGI para producción
│   ├── wsgi.py                   # Configuración WSGI para servidor
│   ├── settings.py               # Configuración de Django
│   ├── urls.py                   # Rutas (URLs) de la aplicación
│   ├── views.py                  # Lógica de negocio (vistas)
│   ├── models.py                 # Modelos de base de datos
│   ├── route_calculator.py       # Algoritmo Dijkstra para rutas
│   │
│   ├── migrations/               # Migraciones de base de datos
│   │   ├── 0001_initial.py      # Primera migración
│   │   ├── 0002_cartitem.py     # Modelo de carrito
│   │   └── 0003_deliveryestimate.py  # Estimación de entrega
│   │
│   ├── templates/                # Plantillas HTML
│   │   ├── core/
│   │   │   └── index.html       # Página de inicio
│   │   ├── auth/
│   │   │   └── login.html       # Login/Registro
│   │   ├── client/
│   │   │   ├── dashboard.html   # Dashboard cliente
│   │   │   ├── create_order.html # Crear orden
│   │   │   ├── orders.html      # Ver órdenes
│   │   │   └── account.html     # Cuenta cliente
│   │   └── admin/
│   │       ├── dashboard.html   # Dashboard admin
│   │       ├── services.html    # Gestión de servicios
│   │       └── account.html     # Cuenta admin
│   │
│   └── __pycache__/             # Archivos compilados
│
├── db.sqlite3                     # Base de datos SQLite
├── manage.py                      # Script de gestión Django
├── initialize_routes.py           # Script para inicializar rutas
├── setup_db.py                    # Script de configuración
├── verify_setup.py                # Script de verificación
│
└── Documentación
    ├── README.md
    ├── DOCUMENTACION_COMPLETA.md  # Este archivo
    └── ...
```

---

## Explicación de Archivos

### 1. `manage.py` - Gestor de Django

**¿Qué es?**
Script principal para administrar la aplicación Django.

**Funciones:**
- `python manage.py runserver` - Inicia servidor de desarrollo
- `python manage.py migrate` - Aplica cambios en BD
- `python manage.py makemigrations` - Crea migraciones
- `python manage.py createsuperuser` - Crea usuario admin
- `python manage.py shell` - Abre consola interactiva

**Ubicación:** Raíz del proyecto
**Uso:** `python manage.py [comando]`

---

### 2. `amazoncito/settings.py` - Configuración del Proyecto

**¿Qué es?**
Archivo de configuración global de Django.

**Configuraciones importantes:**

```python
DEBUG = True                    # Modo debug (True en desarrollo)
INSTALLED_APPS = [
    'django.contrib.admin',    # Panel admin
    'django.contrib.auth',     # Sistema de autenticación
    'django.contrib.sessions', # Gestión de sesiones
    'amazoncito',              # Nuestra aplicación
]

DATABASES = {                  # Configuración de BD
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'es-es'        # Idioma español
TIME_ZONE = 'America/Bogota'   # Zona horaria
```

**Ubicación:** `amazoncito/settings.py`

---

### 3. `amazoncito/urls.py` - Rutas de la Aplicación

**¿Qué es?**
Define todas las URLs (rutas) de la aplicación y las vincula a vistas.

**Rutas principales:**

```python
# Autenticación
path('', views.login_view, name='login')
path('logout/', views.logout_view, name='logout')

# Cliente
path('client/dashboard/', views.client_dashboard, name='client_dashboard')
path('client/create-order/', views.create_order, name='create_order')
path('client/orders/', views.client_orders, name='client_orders')

# Admin
path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard')
path('admin/services/', views.admin_services, name='admin_services')

# API Carrito
path('api/cart/add/', views.add_to_cart, name='add_to_cart')
path('api/cart/get/', views.get_cart, name='get_cart')
path('api/cart/remove/', views.remove_from_cart, name='remove_from_cart')
path('api/cart/update/', views.update_cart_quantity, name='update_cart_quantity')
```

**Ubicación:** `amazoncito/urls.py`

---

### 4. `amazoncito/models.py` - Modelos de Base de Datos

**¿Qué es?**
Define la estructura de datos que se almacena en la base de datos.

**Modelos principales:**

#### a) **UserProfile** - Perfil extendido del usuario
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # 'cliente' o 'admin'
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
```

#### b) **CartItem** - Items del carrito (Base de Datos)
```python
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unique_together = ('user', 'product')  # Un producto por usuario
```
📌 **Estructura usada aquí:** LISTA (cada usuario tiene lista de CartItems)

#### c) **Product** - Productos disponibles
```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
```

#### d) **Order** - Órdenes de compra
```python
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # pendiente, entregado, etc
    destination_city = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=50, unique=True)
```

#### e) **OrderItem** - Items dentro de una orden
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
```
📌 **Estructura usada aquí:** COLA (procesar items en orden)

#### f) **City** - Ciudades para rutas
```python
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
```

#### g) **Route** - Rutas entre ciudades
```python
class Route(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE)
    to_city = models.ForeignKey(City, on_delete=models.CASCADE)
    distance = models.IntegerField()
    estimated_days = models.IntegerField()
```
📌 **Estructura usada aquí:** GRAFO (conexiones entre ciudades)

#### h) **DeliveryEstimate** - Estimación de entrega
```python
class DeliveryEstimate(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    estimated_arrival = models.DateTimeField()
    route_path = models.TextField()  # JSON: ["CDMX", "Puebla", "Cancún"]
    total_distance = models.IntegerField()
```

#### i) **DeliveryHistory** - Historial de entregas
```python
class DeliveryHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivered_at = models.DateTimeField(auto_now_add=True)
```
📌 **Estructura usada aquí:** PILA (último en entrar, primero a consultar)

### Estructuras de Datos en models.py

También hay implementaciones puras de estructuras:

```python
class Node:
    """Nodo para listas enlazadas"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Lista enlazada simple"""
    def append(self, data): ...
    def to_list(self): ...

class Queue:
    """Cola - FIFO (First In, First Out)"""
    def enqueue(self, item): ...
    def dequeue(self): ...

class Stack:
    """Pila - LIFO (Last In, First Out)"""
    def push(self, item): ...
    def pop(self): ...

class HashTable:
    """Tabla hash con polinomio de direccionamiento"""
    def hash_polynomial(self, key): ...

class Graph:
    """Grafo para rutas"""
    def add_vertex(self, vertex): ...
    def add_edge(self, v1, v2, weight): ...
    def bfs_shortest_path(self, start, end): ...
```

**Ubicación:** `amazoncito/models.py`

---

### 5. `amazoncito/views.py` - Lógica de Negocio

**¿Qué es?**
Contiene la lógica de cada funcionalidad: qué datos obtener, cómo procesarlos y qué mostrar.

**Vistas principales:**

#### a) Autenticación
```python
def login_view(request):
    """Permite login y registro de usuarios"""
    # Si POST: valida credenciales y hace login
    # Si GET: muestra formulario

def logout_view(request):
    """Cierra la sesión del usuario"""

def redirect_by_role(request):
    """Redirige según rol: cliente → dashboard, admin → admin"""
```

#### b) Dashboard del Cliente
```python
def client_dashboard(request):
    """Muestra productos organizados por categoría"""
    # Obtiene categorías
    categories = Category.objects.all()
    # Agrupa productos por categoría
    for category in categories:
        products_by_category[category.name] = category.products.all()
```

#### c) Crear Orden
```python
def create_order(request):
    """Crea una nueva orden con los productos del carrito"""
    # 1. Obtiene productos seleccionados
    # 2. Crea objeto Order
    # 3. Crea OrderItems para cada producto
    # 4. LLAMA A DIJKSTRA para calcular ruta
    # 5. Crea DeliveryEstimate
    # 6. Limpia el carrito
    # 7. Retorna tracking_number y estimated_days
```

**¡Aquí se usa DIJKSTRA!:**
```python
from .route_calculator import get_delivery_estimate

estimate = get_delivery_estimate(destination_city)
# Retorna: {route, distance, estimated_days, arrival_datetime}

DeliveryEstimate.objects.create(
    order=order,
    estimated_arrival=estimate['arrival_datetime'],
    route_path=json.dumps(estimate['route']),
    total_distance=estimate['distance']
)
```

#### d) API Carrito

**Agregar producto:**
```python
def add_to_cart(request):
    """Agrega producto al carrito"""
    # 1. Obtiene product_id y quantity
    # 2. Busca CartItem con (user, product)
    # 3. Si no existe: crea uno
    # 4. Si existe: suma cantidad
    # 5. Retorna JSON con cart_count
```

**Obtener carrito:**
```python
def get_cart(request):
    """Retorna productos en carrito del usuario"""
    # Busca todos los CartItem del usuario
    # Convierte a JSON: {product_id: {name, price, quantity}}
```

**Actualizar cantidad:**
```python
def update_cart_quantity(request):
    """Actualiza cantidad de producto en carrito"""
    # Busca CartItem
    # Actualiza cantidad
    # Calcula nuevo subtotal
```

**Quitar producto:**
```python
def remove_from_cart(request):
    """Elimina producto del carrito"""
    # Busca CartItem con (user, product_id)
    # Lo elimina
    # Retorna nuevo cart_count
```

**Limpiar carrito:**
```python
def clear_cart(request):
    """Elimina todos los productos del carrito"""
    # Borra todos los CartItem del usuario
```

#### e) Dashboard Admin
```python
def admin_dashboard(request):
    """Muestra estadísticas y órdenes recientes"""
    # Total de órdenes
    # Órdenes pendientes
    # Órdenes entregadas
    # Ingreso total
    # Para cada orden: ENRIQUECE con route_info:
        order.route_info = {
            'path': ['CDMX', 'Puebla', 'Cancún'],
            'distance': 1250,
            'arrival': datetime
        }
```

#### f) Servicios Admin
```python
def admin_services(request):
    """Gestiona órdenes"""
    # Si POST action='delete': cancela orden
    # Si POST action='complete': marca como entregada
    # Muestra cola de órdenes pendientes (FIFO)
    pending_orders_queue = Order.objects.filter(status='pendiente').order_by('created_at')
```

**Ubicación:** `amazoncito/views.py`

---

### 6. `amazoncito/route_calculator.py` - Algoritmo Dijkstra

**¿Qué es?**
Implementa el algoritmo de Dijkstra para encontrar la ruta más corta entre ciudades.

**Problema que resuelve:**
¿Cuál es la ruta más rápida desde Ciudad de México a Cancún?

**Algoritmo Dijkstra:**

```
Entrada: ciudad_inicio, ciudad_fin
Salida: ruta más corta, distancia total, días

1. Inicializar:
   - distancias[todas] = infinito
   - distancias[inicio] = 0
   - cola_prioridad = [(0, inicio)]
   
2. Mientras haya ciudades en cola:
   - Sacar ciudad con menor distancia
   - Si es el destino: TERMINAR
   - Para cada ciudad vecina:
     - Calcular nueva_distancia = distancia_actual + arista
     - Si nueva_distancia < distancia_guardada:
       - Actualizar distancia
       - Agregar a cola_prioridad
   
3. Reconstruir ruta desde inicio hasta fin
```

**Implementación en Python:**

```python
class RouteCalculator:
    def _build_graph(self):
        """Construye grafo: {ciudad: [(vecino, distancia, días), ...]}"""
        graph = {}
        routes = Route.objects.all()
        for route in routes:
            # Agregar en ambas direcciones (grafo NO dirigido)
            graph[route.from_city.name].append(
                (route.to_city.name, route.distance, route.estimated_days)
            )
            graph[route.to_city.name].append(
                (route.from_city.name, route.distance, route.estimated_days)
            )
        return graph
    
    def dijkstra(self, start, end):
        """Encuentra ruta más corta"""
        import heapq
        
        # Inicializar
        distances = {city: float('inf') for city in self.graph}
        distances[start] = 0
        total_days = {city: float('inf') for city in self.graph}
        total_days[start] = 0
        previous = {city: None for city in self.graph}
        
        # Cola de prioridad: (distancia, ciudad)
        heap = [(0, start)]
        visited = set()
        
        # Procesar
        while heap:
            current_distance, current_city = heapq.heappop(heap)
            
            if current_city in visited:
                continue
            visited.add(current_city)
            
            if current_city == end:
                break
            
            # Revisar vecinos
            for neighbor, distance, days in self.graph[current_city]:
                if neighbor not in visited:
                    new_distance = distances[current_city] + distance
                    new_days = total_days[current_city] + days
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        total_days[neighbor] = new_days
                        previous[neighbor] = current_city
                        heapq.heappush(heap, (new_distance, neighbor))
        
        # Reconstruir ruta
        route = []
        current = end
        while current is not None:
            route.append(current)
            current = previous[current]
        route.reverse()
        
        return (route, distances[end], total_days[end])
```

**Ejemplo de ejecución:**

```
Grafo:
CDMX ─── 500km/1día ─── Guadalajara
 │                            │
 ├─── 300km/1día ─── Puebla ──┤
      │                        │
      └─── 600km/2días ─── Mérida ─── 400km/2días ─── Cancún
                               │
                               └─── 800km/3días ─── Merida

Consulta: CDMX → Cancún

Ejecución:
1. Inicio: distancias[CDMX]=0
2. Procesa CDMX:
   - Guadalajara: 500
   - Puebla: 300
   - Mérida: 600
3. Procesa Puebla (menor=300):
   - Mérida: min(600, 300+600) = 600
   - Cancún: ∞ (no vecino directo)
4. Procesa Guadalajara (=500):
   - Mérida: min(600, 500+1000) = 600
5. Procesa Mérida (=600):
   - Cancún: 600+400 = 1000 km, 4 días

Resultado:
- Ruta: [CDMX, Puebla, Mérida, Cancún]
- Distancia: 1250 km
- Días: 4
```

**Uso en la aplicación:**

```python
def get_delivery_estimate(destination_city):
    calculator = RouteCalculator()
    result = calculator.dijkstra('Ciudad de Mexico', destination_city)
    
    if result:
        route, distance, days = result
        arrival = datetime.now() + timedelta(days=days)
        return {
            'route': route,
            'distance': distance,
            'estimated_days': days,
            'arrival_datetime': arrival
        }
```

**Ubicación:** `amazoncito/route_calculator.py`

---

### 7. `amazoncito/templates/` - Plantillas HTML

**¿Qué es?**
Archivos HTML que muestran la interfaz al usuario. Django reemplaza variables `{{ variable }}` con datos reales.

#### a) `client/create_order.html` - Crear Orden

**Funciones JavaScript:**

```javascript
// CARRITO EN MEMORIA (LOCAL STATE)
let cart = {};  // {product_id: {name, price, quantity}, ...}

// AGREGAR AL CARRITO
function addToCartServer(productId, productName, productPrice) {
    // 1. Actualizar local cart inmediatamente
    if (cart[productId]) {
        cart[productId].quantity++;
    } else {
        cart[productId] = {
            id: productId,
            name: productName,
            price: productPrice,
            quantity: 1
        };
    }
    
    // 2. Re-renderizar UI
    renderProducts();
    updateCart();
    
    // 3. Enviar a servidor (async)
    fetch('/api/cart/add/', {
        method: 'POST',
        body: new FormData(`...`)
    });
}

// RENDERIZAR PRODUCTOS EN TABLA
function renderProducts() {
    let html = '';
    for (let productId in cart) {
        let item = cart[productId];
        html += `
            <tr>
                <td>${item.name}</td>
                <td>$${item.price}</td>
                <td>
                    <input type="number" value="${item.quantity}" 
                           onchange="updateCartQuantity(${productId}, this.value)">
                </td>
                <td>$${item.price * item.quantity}</td>
                <td>
                    <button onclick="removeFromCart(${productId})">Quitar</button>
                </td>
            </tr>
        `;
    }
    document.getElementById('products-table').innerHTML = html;
}

// ACTUALIZAR CANTIDAD
function updateCartQuantity(productId, newQuantity) {
    cart[productId].quantity = parseInt(newQuantity);
    renderProducts();  // Re-renderizar inmediatamente
    updateCart();      // Actualizar totales
}

// QUITAR DEL CARRITO
function removeFromCart(productId) {
    delete cart[productId];  // Eliminar del objeto
    renderProducts();        // Re-renderizar
    updateCart();            // Actualizar totales
}

// LIMPIAR CARRITO
function clearCartServer() {
    cart = {};               // Vaciar objeto
    renderProducts();        // Re-renderizar
    updateCart();            // Actualizar totales
}

// ACTUALIZAR TOTALES Y CHECKBOX
function updateCart() {
    let total = 0;
    let count = 0;
    
    for (let productId in cart) {
        let item = cart[productId];
        if (document.getElementById(`check-${productId}`).checked) {
            total += item.price * item.quantity;
            count++;
        }
    }
    
    document.getElementById('total-price').textContent = total.toFixed(2);
    document.getElementById('items-count').textContent = count;
}

// CREAR ORDEN
function submitOrder() {
    // 1. Recopilar productos seleccionados
    let selectedProducts = [];
    for (let productId in cart) {
        if (document.getElementById(`check-${productId}`).checked) {
            selectedProducts.push({
                id: productId,
                quantity: cart[productId].quantity
            });
        }
    }
    
    // 2. Obtener ciudad destino
    let destinationCity = document.getElementById('destination-city').value;
    
    // 3. Crear FormData con datos
    let formData = new FormData();
    selectedProducts.forEach((p, i) => {
        formData.append(`product_id`, p.id);
        formData.append(`quantity`, p.quantity);
    });
    formData.append('destination_city', destinationCity);
    
    // 4. Enviar a servidor
    fetch('/client/create-order/', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        // 5. Mostrar éxito con ETA
        alert(`Orden creada: ${data.tracking_number}\nLlegada: ${data.estimated_days} días`);
        // Limpiar
        cart = {};
        renderProducts();
    });
}
```

**Flujo:**
```
Usuario selecciona producto
    ↓
addToCartServer() - Actualiza cart{}
    ↓
renderProducts() - Re-renderiza tabla
    ↓
Usuario cambia cantidad
    ↓
updateCartQuantity() - Actualiza cart{}
    ↓
renderProducts() + updateCart() - Re-renderiza
    ↓
Usuario hace click "Crear Orden"
    ↓
submitOrder() - Recopila datos
    ↓
Envía a views.create_order()
    ↓
Servidor calcula DIJKSTRA
    ↓
Retorna JSON con tracking_number, estimated_days
    ↓
Mostrar al usuario con ETA
```

#### b) `admin/dashboard.html` - Panel Admin

**Tabla de órdenes:**

```html
<table>
    <thead>
        <tr>
            <th>Tracking</th>
            <th>Cliente</th>
            <th>Total</th>
            <th>Status</th>
            <th>Ruta Estimada</th>      <!-- Nueva -->
            <th>ETA</th>                 <!-- Nueva -->
        </tr>
    </thead>
    <tbody>
        {% for order in recent_orders %}
        <tr>
            <td>{{ order.tracking_number }}</td>
            <td>{{ order.user.username }}</td>
            <td>${{ order.total_price }}</td>
            <td>{{ order.status }}</td>
            <td>
                {% if order.route_info %}
                    {{ order.route_info.path|join:" → " }}
                    <br>{{ order.route_info.distance }} km
                {% else %}
                    No calculada
                {% endif %}
            </td>
            <td>
                {% if order.route_info %}
                    {{ order.route_info.arrival|date:"d/m H:i" }}
                {% else %}
                    -
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

**Ubicación:** `amazoncito/templates/`

---

## Estructuras de Datos Utilizadas

### 1. **LISTA / ARRAY**

**¿Dónde se usa?**
- Carrito: `cart = {}`
- Productos en orden: `selectedProducts = []`
- Items en tabla HTML

**Implementación:**
```python
# En Python
cart_items = CartItem.objects.filter(user=request.user)
for item in cart_items:  # Iterar como lista
    print(item.product.name)

# En JavaScript
let cart = {};
cart[productId] = {name, price, quantity}  // Agregar
delete cart[productId]  // Quitar
for (let id in cart) {}  // Iterar
```

**Complejidad:**
- Acceso: O(1)
- Búsqueda: O(n)
- Inserción: O(1)
- Eliminación: O(1)

---

### 2. **PILA (Stack) - LIFO**

**¿Dónde se usa?**

#### a) **Historial de entregas** (DeliveryHistory)
```python
class DeliveryHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivered_at = models.DateTimeField(auto_now_add=True)
```

Usar como pila:
```python
# PUSH: Agregar entrega
DeliveryHistory.objects.create(order=order, notes="Entregado")

# POP: Obtener última entrega
last_delivery = DeliveryHistory.objects.filter(
    order=order
).order_by('-delivered_at').first()

# PEEK: Ver última sin eliminar
last = DeliveryHistory.objects.filter(...).latest('delivered_at')
```

#### b) **Historial de navegación en usuario**
La navega por: Dashboard → Crear Orden → Confirmación
Pila: [Dashboard, Crear Orden, Confirmación]
Volver: Pop = Confirmación → Crear Orden → Dashboard

**Implementación pura en models.py:**
```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)  # Agregar al final
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()  # Quitar último
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]  # Ver último
        return None
```

**Complejidad:**
- Push: O(1)
- Pop: O(1)
- Peek: O(1)

---

### 3. **COLA (Queue) - FIFO**

**¿Dónde se usa?**

#### a) **Procesamiento de órdenes pendientes**
```python
# En admin/services
pending_orders_queue = Order.objects.filter(
    status='pendiente'
).order_by('created_at')  # Primera en entrar

for order in pending_orders_queue:
    # Procesar: FIFO
    process_order(order)
    order.status = 'procesando'
    order.save()
```

#### b) **Items en una orden**
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

# En views.py
order_queue = []
for product_id, quantity in zip(items, quantities):
    # ENQUEUE
    order_queue.append({
        'product': product.name,
        'quantity': qty,
        'price': float(price)
    })
    # Crear OrderItem
    OrderItem.objects.create(order=order, product=product, ...)

# DEQUEUE cuando se procesa la orden
while order_queue:
    item = order_queue.pop(0)  # Primero en entrar
    send_notification(item)
```

**Implementación pura en models.py:**
```python
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)  # Agregar al final
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)  # Quitar del inicio
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

**Complejidad:**
- Enqueue: O(1)
- Dequeue: O(n) en lista, O(1) en deque
- Búsqueda: O(n)

---

### 4. **TABLA HASH (Hash Table)**

**¿Dónde se usa?**

#### a) **Diccionario de carrito** (JavaScript)
```javascript
let cart = {};  // Hash table
cart[productId] = {name, price, quantity}

// Búsqueda O(1)
if (cart[productId]) { ... }

// Inserción O(1)
cart[newProductId] = {...}

// Eliminación O(1)
delete cart[productId]
```

#### b) **Diccionario de productos por categoría** (Python)
```python
products_by_category = {}
for category in categories:
    products_by_category[category.name] = list(category.products.all())

# Búsqueda O(1)
products = products_by_category['Electrónica']
```

**Implementación pura en models.py:**
```python
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def hash_polynomial(self, key):
        """Función hash con polinomio de direccionamiento"""
        hash_value = 0
        p = 31
        p_pow = 1
        for char in str(key):
            hash_value = (hash_value + (ord(char) * p_pow)) % (10**9 + 9)
            p_pow = (p_pow * p) % (10**9 + 9)
        return hash_value % self.size
    
    def insert(self, key, value):
        index = self.hash_polynomial(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
    
    def search(self, key):
        index = self.hash_polynomial(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
```

**Complejidad:**
- Búsqueda: O(1) promedio, O(n) peor caso
- Inserción: O(1) promedio, O(n) peor caso
- Eliminación: O(1) promedio, O(n) peor caso

---

### 5. **LISTA ENLAZADA (Linked List)**

**¿Dónde se usa?**

#### a) **Secuencia de notificaciones**
Cada notificación apunta a la siguiente:

```
[Notificación 1] → [Notificación 2] → [Notificación 3] → None
```

#### b) **Historial de cambios en estado de orden**
```python
class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

# Usar
history = LinkedList()
history.append({'status': 'pendiente', 'timestamp': now})
history.append({'status': 'procesando', 'timestamp': now})
history.append({'status': 'entregado', 'timestamp': now})
```

**Complejidad:**
- Acceso: O(n)
- Búsqueda: O(n)
- Inserción: O(1) si conoces posición
- Eliminación: O(1) si conoces nodo

---

### 6. **GRAFO (Graph) - ¡MÁS IMPORTANTE!**

**¿Dónde se usa?**

**Red de rutas de entrega:**

```
Ciudad de Mexico ──(500km, 1día)── Guadalajara
       │                                  │
       │                                  │
   (300km)                            (1000km)
   1día                              2días
       │                                  │
       ▼                                  ▼
    Puebla ───(600km, 2días)─────────────→ Mérida
       │                                  │
       │                                  │
   (800km)                            (400km)
   3días                              2días
       │                                  │
       ▼                                  ▼
    Cancún ◄──(1250km, 4días)────────────┘
```

**Tipos de Grafo:**

- **Dirigido:** Las aristas tienen dirección (A→B ≠ B→A)
- **No dirigido:** Las aristas van en ambas direcciones (A↔B)
- **Ponderado:** Cada arista tiene peso (distancia, tiempo)
- **No ponderado:** Todas las aristas tienen peso 1

En Amazoncito: **Grafo NO dirigido, ponderado**

**Implementación en route_calculator.py:**

```python
class RouteCalculator:
    def _build_graph(self):
        """Grafo: {ciudad: [(vecino, distancia, días), ...]}"""
        graph = {}
        for route in Route.objects.all():
            from_city = route.from_city.name
            to_city = route.to_city.name
            
            # Agregar en AMBAS direcciones
            if from_city not in graph:
                graph[from_city] = []
            if to_city not in graph:
                graph[to_city] = []
            
            # No dirigido: A→B y B→A
            graph[from_city].append((to_city, route.distance, route.estimated_days))
            graph[to_city].append((from_city, route.distance, route.estimated_days))
        
        return graph
```

**Recorridos:**

1. **BFS (Breadth-First Search)** - Busca en anchura
```python
from collections import deque

def bfs(graph, start, end):
    """Encuentra ruta sin considerar pesos"""
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()  # DEQUEUE
        
        if node == end:
            return path
        
        for neighbor, _, _ in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))  # ENQUEUE
    
    return None
```

2. **DFS (Depth-First Search)** - Búsqueda en profundidad
```python
def dfs(graph, node, end, visited, path):
    """Busca en profundidad"""
    if node == end:
        return path + [node]
    
    visited.add(node)
    
    for neighbor, _, _ in graph.get(node, []):
        if neighbor not in visited:
            result = dfs(graph, neighbor, end, visited, path + [node])
            if result:
                return result
    
    return None
```

3. **DIJKSTRA** - Encuentra camino más corto (¡USADO EN AMAZONCITO!)
```python
def dijkstra(graph, start, end):
    """Encuentra ruta más CORTA considerando pesos"""
    import heapq
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    
    heap = [(0, start)]
    visited = set()
    
    while heap:
        current_distance, current = heapq.heappop(heap)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == end:
            break
        
        for neighbor, weight, _ in graph.get(current, []):
            if neighbor not in visited:
                new_distance = distances[current] + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(heap, (new_distance, neighbor))
    
    # Reconstruir ruta
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path if distances[end] != float('inf') else None
```

**Complejidad Dijkstra:**
- Con lista: O(V²)
- Con heap (binary): O((V + E) log V)
- En Amazoncito: O((22 + 57) * log 22) ≈ O(79 * 4.5) ≈ O(355) operaciones

---

## Flujo Completo del Sistema

### Flujo 1: Cliente Compra Productos

```
1. Cliente accede: http://127.0.0.1:8000/
                ↓
2. views.login_view()
   - Si no autenticado: mostrar login.html
   - Si autenticado: redirigir según rol
                ↓
3. Client Dashboard
   - views.client_dashboard()
   - Obtiene categorías y productos
   - Renderiza templates/client/dashboard.html
                ↓
4. Cliente hace click "Crear Orden"
   - Navega a: /client/create-order/
   - views.create_order() (GET)
   - Obtiene CartItems del usuario
   - Convierte a JSON para JavaScript
   - Renderiza create_order.html
                ↓
5. Cliente selecciona productos
   - JavaScript addToCartServer(productId)
   - Actualiza cart{} en memoria
   - Llama renderProducts() inmediatamente
   - POST a /api/cart/add/
   - views.add_to_cart() crea/actualiza CartItem en BD
                ↓
6. Cliente ajusta cantidades
   - JavaScript updateCartQuantity()
   - Actualiza cart{} en memoria
   - Renderiza tabla
                ↓
7. Cliente quita producto
   - removeFromCart(productId)
   - Borra del cart{}
   - Renderiza tabla
                ↓
8. Cliente selecciona ciudad y hace click "Comprar"
   - JavaScript submitOrder()
   - Recopila productos seleccionados
   - POST a /client/create-order/
                ↓
9. views.create_order() (POST)
   - Crea Order
   - Para cada producto: crea OrderItem
   - LLAMA A DIJKSTRA:
     from .route_calculator import get_delivery_estimate
     estimate = get_delivery_estimate('Cancún')
   - RouteCalculator.dijkstra('Ciudad de Mexico', 'Cancún')
   - Retorna ruta más corta: [CDMX, Puebla, Mérida, Cancún]
   - Calcula días y distancia
   - Crea DeliveryEstimate
   - Borra CartItems
   - Retorna JSON con tracking_number, estimated_days
                ↓
10. Cliente recibe confirmación
    - Muestra tracking_number
    - Muestra "Llegará en X días"
```

### Flujo 2: Admin Ve Órdenes y Rutas

```
1. Admin accede: http://127.0.0.1:8000/admin/dashboard/
                ↓
2. views.admin_dashboard()
   - Obtiene últimas 10 órdenes
   - Para cada orden:
     - Accede a order.delivery_estimate
     - Extrae: route_path, total_distance, estimated_arrival
     - Crea diccionario route_info:
       {
           'path': ['CDMX', 'Puebla', 'Mérida', 'Cancún'],
           'distance': 1250,
           'arrival': datetime(2025, 11, 27, 21, 16)
       }
   - Pasa al contexto
                ↓
3. Renderiza admin/dashboard.html
   - Muestra tabla con columnas:
     - Tracking
     - Cliente
     - Total
     - Status
     - Ruta Estimada: "CDMX → Puebla → Mérida → Cancún"
     - ETA: "27/11 21:16"
                ↓
4. Admin puede completar o cancelar orden
   - Click en "Completar": POST /admin/services/
     - action='complete'
     - views.admin_services()
     - order.status = 'entregado'
     - Crea DeliveryHistory (pila)
     - Crea NotificationMessage
   
   - Click en "Cancelar": POST /admin/services/
     - action='delete'
     - order.status = 'cancelado'
     - Envía mensaje de cancelación
```

### Flujo 3: Procesamiento de Orden Pendiente

```
Órdenes Pendientes (Cola FIFO):
[Orden 1 - 10:00] → [Orden 2 - 10:05] → [Orden 3 - 10:10]

1. Admin ve /admin/services/
   - pending_orders_queue = Order.objects.filter(
       status='pendiente'
     ).order_by('created_at')
   
   Muestra (FIFO):
   - Orden 1 (primera en entrar, primera en procesar)
   - Orden 2
   - Orden 3

2. Admin procesa Orden 1
   - Click "Completar"
   - DEQUEUE: Orden 1 se elimina de pendientes
   - status = 'entregado'
   - PUSH a DeliveryHistory (pila)
   
   Ahora cola es:
   [Orden 2 - 10:05] → [Orden 3 - 10:10]

3. Historial de entregas (Pila LIFO):
   TOP: [Orden 1 entregado]
        [Orden 0 entregado]
        [Orden -1 entregado]
   
   Para ver última entrega: POP = Orden 1
```

---

## Base de Datos

### Modelo Relacional

```
┌─────────────────────┐
│        User         │ (Django auth)
│─────────────────────│
│ id (PK)             │
│ username (Unique)   │
│ password            │
│ email               │
└──────────┬──────────┘
           │ 1:1
           ▼
┌─────────────────────┐
│    UserProfile      │
│─────────────────────│
│ id (PK)             │
│ user_id (FK, U)     │
│ role                │
│ address             │
│ phone               │
└─────────────────────┘

┌─────────────────────┐
│      Category       │
│─────────────────────│
│ id (PK)             │
│ name (Unique)       │
│ description         │
└──────────┬──────────┘
           │ 1:N
           ▼
┌─────────────────────┐
│      Product        │
│─────────────────────│
│ id (PK)             │
│ category_id (FK)    │
│ name                │
│ price (Decimal)     │
│ weight (Decimal)    │
└──────────┬──────────┘
           │ N:M (through OrderItem)
           │ 1:N (through CartItem)
           │
           ├─────────────────────────┐
           │                         │
           ▼                         ▼
    ┌─────────────────┐    ┌──────────────────┐
    │   OrderItem     │    │    CartItem      │
    ├─────────────────┤    ├──────────────────┤
    │ id (PK)         │    │ id (PK)          │
    │ order_id (FK)   │    │ user_id (FK)     │
    │ product_id (FK) │    │ product_id (FK)  │
    │ quantity        │    │ quantity         │
    │ price           │    │ added_at         │
    │                 │    │ updated_at       │
    │ (COLA)          │    │ U(user, product) │
    └──────┬──────────┘    └──────────────────┘
           │ N:1
           ▼
┌─────────────────────────┐
│        Order            │
│─────────────────────────│
│ id (PK)                 │
│ user_id (FK)            │
│ status                  │
│ destination_city        │
│ tracking_number (Unique)│
│ total_price             │
│ created_at              │
│ updated_at              │
│ cancellation_message    │
│                         │
│ (Pedido de cliente)     │
└──────────┬──────────────┘
           │ 1:1
           ▼
┌──────────────────────────┐
│  DeliveryEstimate        │
│──────────────────────────│
│ id (PK)                  │
│ order_id (FK, U)         │
│ estimated_arrival (DT)   │
│ route_path (JSON)        │
│ total_distance (km)      │
│                          │
│ (Ruta calculada)         │
└──────────────────────────┘

┌──────────────────────┐
│   DeliveryHistory    │
│──────────────────────│
│ id (PK)              │
│ order_id (FK)        │
│ delivered_at         │
│ notes                │
│                      │
│ (Pila de entregas)   │
└──────────────────────┘

┌──────────────────────┐
│  NotificationMessage │
│──────────────────────│
│ id (PK)              │
│ user_id (FK)         │
│ order_id (FK, N)     │
│ message              │
│ is_read              │
│ created_at           │
└──────────────────────┘

Estructuras de Rutas (GRAFO):

┌─────────────────────┐
│        City         │
│─────────────────────│
│ id (PK)             │
│ name (Unique)       │
└──────────┬──────────┘
           │ 1:N (from_routes)
           │ 1:N (to_routes)
           ▼
┌──────────────────────┐
│       Route          │
│──────────────────────│
│ id (PK)              │
│ from_city_id (FK)    │
│ to_city_id (FK)      │
│ distance (km)        │
│ estimated_days       │
│                      │
│ (Arista del grafo)   │
└──────────────────────┘
```

### Ejemplo de Datos

```
Cities (Vértices del grafo):
- Ciudad de Mexico
- Guadalajara
- Monterrey
- Cancún
- Mérida
- Puebla
- Veracruz
- Querétaro
- San Luis Potosí
- Toluca

Routes (Aristas):
CDMX → Guadalajara: 500 km, 1 día
CDMX → Puebla: 300 km, 1 día
CDMX → Querétaro: 200 km, 1 día
CDMX → Toluca: 65 km, 1 día
Puebla → Mérida: 600 km, 2 días
Mérida → Cancún: 400 km, 2 días
... (57 rutas totales)

Order (Ejemplo):
- id: 1
- user: juan_cliente
- status: pendiente
- destination_city: Cancún
- tracking_number: A1B2C3D4E5F6
- total_price: $120.00
- created_at: 2025-11-23 14:30:00

OrderItem (Items de orden):
- orden: 1
- producto: Caja Mediana
- quantity: 2
- price: $50.00

CartItem (Items en carrito):
- user: maria_cliente
- product: Sobre Estándar
- quantity: 5
- added_at: 2025-11-23 14:20:00

DeliveryEstimate (Calculada por Dijkstra):
- order: 1
- estimated_arrival: 2025-11-27 21:16:00
- route_path: ["Ciudad de Mexico", "Puebla", "Mérida", "Cancún"]
- total_distance: 1300 km
```

---

## Resumen Técnico

### Tecnologías

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Backend | Django | 5.2.6 |
| Lenguaje | Python | 3.13 |
| Base de Datos | SQLite | 3.x |
| Frontend | HTML/CSS/JS | ES6+ |
| Algoritmo | Dijkstra | C(V+E)logV |

### Estructuras de Datos

| Estructura | Uso | Complejidad |
|-----------|-----|------------|
| Lista | Carrito, Productos | O(1) acceso, O(n) búsqueda |
| Pila | Historial entregas | O(1) push/pop |
| Cola | Órdenes pendientes | O(1) enqueue, O(n) dequeue |
| Hash Table | Productos por categoría | O(1) búsqueda |
| Grafo | Red de rutas | O((V+E)logV) Dijkstra |
| Lista Enlazada | Secuencias | O(n) acceso |

### URLs Principales

```
/ .......................... Login/Registro
/client/dashboard/ .......... Dashboard Cliente
/client/create-order/ ....... Crear Orden
/client/orders/ ............. Ver Órdenes
/admin/dashboard/ ........... Dashboard Admin
/admin/services/ ............ Gestionar Órdenes
/api/cart/add/ .............. Agregar al carrito
/api/cart/get/ .............. Obtener carrito
/api/cart/remove/ ........... Quitar del carrito
/api/cart/clear/ ............ Limpiar carrito
/api/cart/update/ ........... Actualizar cantidad
```

---

## Comandos Útiles

```powershell
# Iniciar servidor
python manage.py runserver

# Ver base de datos
python manage.py shell
>>> from amazoncito.models import *
>>> Order.objects.all()
>>> for order in Order.objects.all():
...     print(order.tracking_number, order.destination_city)

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver historial de migraciones
python manage.py showmigrations

# Crear superusuario
python manage.py createsuperuser

# Revertir migración
python manage.py migrate amazoncito [número]

# Vaciar base de datos (cuidado!)
python manage.py flush

# Inicializar rutas
python initialize_routes.py
```

---

## Troubleshooting

### Error: "No such table"
```
Solución:
python manage.py migrate
```

### Error: "Module not found"
```
Solución:
pip install django==5.2.6
pip install asgiref==3.8.1
pip install sqlparse==0.5.0
```

### Puerto 8000 ya en uso
```
Solución:
python manage.py runserver 8001
# O matar proceso
taskkill /PID [pid] /F
```

### CSRF Token error
Verificar que:
1. El formulario incluya `{% csrf_token %}`
2. La solicitud POST tenga el header CSRF correcto

---

## Conclusión

El sistema **Amazoncito** demuestra la aplicación práctica de:

✅ **Estructuras de Datos:**
- Listas para carrito y productos
- Pilas para historial de entregas
- Colas para procesamiento FIFO
- Tablas hash para búsqueda rápida
- Grafos para redes de rutas
- Listas enlazadas para secuencias

✅ **Algoritmos:**
- Dijkstra para ruta más corta
- BFS/DFS para navegación (en modelo Graph)

✅ **Patrones de Desarrollo:**
- MVC (Model-View-Controller)
- API REST
- ORM (Django ORM)
- Autenticación y autorización

✅ **Tecnologías:**
- Django framework
- SQLite database
- HTML/CSS/JavaScript frontend
- Asynchronous operations

Este proyecto es un **ejemplo completo de cómo las estructuras de datos y algoritmos se usan en aplicaciones reales de producción**.

---

**¡Sistema completamente funcional y documentado!** 🎉
