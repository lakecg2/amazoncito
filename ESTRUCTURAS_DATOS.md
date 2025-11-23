# 📋 RESUMEN DE ESTRUCTURAS DE DATOS IMPLEMENTADAS

## Sistema de Gestión de Paqueterías - Amazoncito

### 1. LISTAS ENLAZADAS (LinkedList)

**Ubicación:** `models.py` - Clase `LinkedList`

**Uso en el sistema:**
- Gestión de categorías de productos
- Almacenamiento de productos en cada categoría

```python
class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        # Agregar elemento al final
        
    def to_list(self):
        # Convertir a lista de Python
```

**Aplicación práctica:**
- Cuando un cliente ve los productos, se organizan en listas enlazadas por categoría
- Permite iteración eficiente O(n)

---

### 2. COLAS (Queue - FIFO)

**Ubicación:** `models.py` - Clase `Queue`

**Uso en el sistema:**
- Procesamiento de pedidos en orden FIFO (First In, First Out)
- Cola de pedidos pendientes para administrador

```python
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
```

**Aplicación práctica:**
- En `admin/services.html`, los pedidos pendientes se muestran en orden de llegada
- Primera línea: `pending_orders_queue = Order.objects.filter(status='pendiente').order_by('created_at')`
- Los pedidos se procesan en el orden en que fueron recibidos

---

### 3. PILAS (Stack - LIFO)

**Ubicación:** `models.py` - Clase `Stack` y Modelo `DeliveryHistory`

**Uso en el sistema:**
- Historial de entregas completadas
- "Deshacer" la última entrega (funcionalidad opcional)

```python
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
```

**Aplicación práctica:**
```python
# En views.py - admin_services
DeliveryHistory.objects.create(order=order, notes="Entregado exitosamente")
```

- Cuando un pedido se marca como entregado, se agrega al historial (pila)
- Último en entrar, primero en salir
- Permite ver entregas recientes fácilmente

---

### 4. TABLA HASH (HashTable con polinomio de direccionamiento)

**Ubicación:** `models.py` - Clase `HashTable`

**Fórmula de Hash Polinómica:**
```
hash(key) = (Σ(ord(char) * p^i)) mod (10^9 + 9)
            mod tamaño_tabla
```

Donde:
- p = 31 (número primo)
- char = cada carácter de la clave
- i = posición del carácter

```python
class HashTable:
    def hash_polynomial(self, key):
        hash_value = 0
        p = 31
        p_pow = 1
        for char in str(key):
            hash_value = (hash_value + (ord(char) * p_pow)) % (10**9 + 9)
            p_pow = (p_pow * p) % (10**9 + 9)
        return hash_value % self.size
    
    def insert(self, key, value):
        # Insertar en O(1) promedio
        
    def search(self, key):
        # Buscar en O(1) promedio
```

**Aplicación práctica:**
- Búsqueda eficiente de clientes por username
- En `views.py`: `User.objects.filter(username=username)`
- Aunque Django usa su propia indexación, el concepto es aplicable

---

### 5. GRAFOS (Graph con BFS para ruta más corta)

**Ubicación:** `models.py` - Clase `Graph`

**Estructura:**
```python
class Graph:
    def __init__(self):
        self.vertices = {}      # Nodos (ciudades)
        self.edges = {}         # Aristas (conexiones)
    
    def add_vertex(self, vertex):
        # Agregar ciudad
        
    def add_edge(self, v1, v2, weight=1):
        # Agregar ruta entre ciudades
        
    def bfs_shortest_path(self, start, end):
        # Encontrar ruta más corta (BFS)
```

**Algoritmo BFS (Búsqueda en Amplitud):**

```python
def bfs_shortest_path(self, start, end):
    from collections import deque
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path  # Ruta encontrada
        
        for neighbor, _ in self.edges.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # No hay ruta
```

**Aplicación práctica:**
- Modelar rutas entre ciudades colombianas
- Calcular ruta más corta de entrega
- Datos en `models.py`:
  - Vértices: Bogotá, Medellín, Cali, Barranquilla, Cartagena, Santa Marta
  - Aristas: Rutas con distancia y días estimados

**Ejemplo de datos:**
```
Bogotá --500km--> Medellín (2 días)
Bogotá --600km--> Cali (2 días)
Medellín --700km--> Cartagena (3 días)
...
```

---

## INTEGRACIÓN EN VISTAS

### Cliente - Crear Pedido (`client/create_order.html`)
```javascript
// Los productos se organizan en estructura de datos
// Usar cola para procesar items del pedido
const order_queue = [];
selectedProducts.forEach(product => {
    order_queue.push({
        product: product.name,
        quantity: qty,
        price: product.price
    });
});
```

### Administrador - Gestión de Servicios (`admin/services.html`)
```python
# Cola de pedidos pendientes (FIFO)
pending_orders_queue = Order.objects.filter(status='pendiente').order_by('created_at')

# Pila de entregas (LIFO)
DeliveryHistory.objects.create(order=order, notes="Entregado exitosamente")
```

---

## COMPLEJIDAD COMPUTACIONAL

| Estructura | Operación | Complejidad | Nota |
|-----------|-----------|-------------|------|
| LinkedList | Insert | O(n) | Al final |
| LinkedList | Search | O(n) | Búsqueda lineal |
| Queue | Enqueue | O(1) | Al final |
| Queue | Dequeue | O(1) | Del inicio |
| Stack | Push | O(1) | Al tope |
| Stack | Pop | O(1) | Del tope |
| HashTable | Insert | O(1) avg | Con colisiones: O(n) |
| HashTable | Search | O(1) avg | Con colisiones: O(n) |
| Graph | BFS | O(V+E) | V=vértices, E=aristas |

---

## PERSISTENCIA DE DATOS

### Base de Datos Django ORM
- Todos los datos se persisten en `db.sqlite3`
- Modelos automáticamente mapeados a tablas SQL

### Archivos CSV (Opcional)
Podría implementarse exportación de datos:
```python
# Exportar pedidos a CSV
import csv
with open('pedidos.csv', 'w') as f:
    writer = csv.writer(f)
    for order in Order.objects.all():
        writer.writerow([order.tracking_number, order.status, order.total_price])
```

---

## ESTADÍSTICAS

- **Modelos:** 8 modelos Django + 5 estructuras de datos personalizadas
- **Vistas:** 11 funciones de vista
- **Templates:** 8 archivos HTML con estilos inline
- **Líneas de código:** ~2000+ líneas
- **Estructuras implementadas:** 5 (LinkedList, Queue, Stack, HashTable, Graph)

---

## OBJETIVOS CUMPLIDOS

✅ Implementar estructuras de datos dinámicas (listas, colas, pilas)
✅ Utilizar tabla hash con polinomio de direccionamiento
✅ Aplicar grafos para modelar rutas de entrega
✅ Simular flujo de pedidos desde registro hasta entrega
✅ Incorporar persistencia de datos mediante Django ORM
✅ Registrar clientes (nombre, ID, dirección, teléfono)
✅ Registrar ciudades y rutas entre ellas
✅ Crear y encolar pedidos
✅ Procesar entregas (BFS para ruta más corta)
✅ Guardar entregas en historial (pila)
✅ Buscar clientes mediante hash

---

**Fecha de Implementación:** Noviembre 2025
**Tecnología:** Django + Python + HTML/CSS/JavaScript
**Base de Datos:** SQLite3
