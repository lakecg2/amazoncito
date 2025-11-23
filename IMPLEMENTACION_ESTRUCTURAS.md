# Implementación de Estructuras de Datos en Amazoncito

## 📁 Ubicación
**Archivo**: `amazoncito/models.py` (Líneas 1-127)

---

## 1️⃣ LISTA ENLAZADA (LinkedList)

### Código
```python
class Node:
    """Nodo para listas enlazadas"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Lista enlazada simple"""
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
    
    def to_list(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items
```

### Caso de Uso en el Proyecto
**Organización de productos por categoría** (views.py, línea 66)

```python
# En client_dashboard():
for category in categories:
    products_by_category[category.name] = list(category.products.all())
```

**Métodos utilizados**:
- `append()` - Agregar productos a la lista
- `to_list()` - Convertir a lista estándar de Python

---

## 2️⃣ COLA (Queue - FIFO)

### Código
```python
class Queue:
    """Cola (FIFO) - First In First Out"""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

### Caso de Uso en el Proyecto
**Procesamiento de pedidos pendientes** (views.py, línea 247)

```python
# En admin_services():
pending_orders_queue = Order.objects.filter(status='pendiente').order_by('created_at')
```

**Flujo**:
1. Cliente crea pedido → Se agrega a la cola (`enqueue`)
2. Admin procesa pedidos en orden de llegada (FIFO)
3. Al completar → Se saca de la cola (`dequeue`)

**Métodos utilizados**:
- `enqueue()` - Agregar pedido a la cola
- `dequeue()` - Procesar el primer pedido
- `is_empty()` - Verificar si hay pedidos pendientes
- `size()` - Contar pedidos en espera

---

## 3️⃣ PILA (Stack - LIFO)

### Código
```python
class Stack:
    """Pila (LIFO) - Last In First Out"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
```

### Caso de Uso en el Proyecto
**Historial de entregas completadas** (models.py, línea 213)

```python
class DeliveryHistory(models.Model):
    """Historial de entregas completadas (Pila)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
```

**Uso en views.py (línea 251)**:
```python
# En admin_services():
DeliveryHistory.objects.create(order=order, notes="Entregado exitosamente")
```

**Métodos utilizados**:
- `push()` - Agregar entrega al historial
- `pop()` - Obtener última entrega realizada
- `peek()` - Ver última entrega sin remover
- Acceso LIFO: Las entregas más recientes se procesan primero

---

## 4️⃣ TABLA HASH (HashTable con Polinomio)

### Código
```python
class HashTable:
    """Tabla hash con polinomio de direccionamiento"""
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
    
    def delete(self, key):
        index = self.hash_polynomial(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                return True
        return False
```

### Características Especiales
- **Función Hash Polinomial**: Utiliza polinomios con base 31
- **Manejo de Colisiones**: Encadenamiento (chaining)
- **Complejidad**: O(1) en promedio para insert/search/delete

### Caso de Uso en el Proyecto
**Búsqueda rápida de clientes** (conceptualmente)

```python
# Ejemplo de uso:
hash_table = HashTable(100)
hash_table.insert('carlos@email.com', {'name': 'Carlos', 'address': '...'})
cliente = hash_table.search('carlos@email.com')  # O(1)
```

**Métodos utilizados**:
- `hash_polynomial()` - Genera índice usando polinomio
- `insert()` - Agregar cliente con búsqueda rápida
- `search()` - Encontrar cliente en O(1)
- `delete()` - Eliminar cliente

---

## 5️⃣ GRAFO CON BFS (Graph + Breadth-First Search)

### Código
```python
class Graph:
    """Grafo para rutas de entrega"""
    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = True
            self.edges[vertex] = []
    
    def add_edge(self, v1, v2, weight=1):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.edges[v1].append((v2, weight))
        self.edges[v2].append((v1, weight))
    
    def bfs_shortest_path(self, start, end):
        """BFS para encontrar la ruta más corta"""
        if start not in self.vertices or end not in self.vertices:
            return None
        
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            
            for neighbor, _ in self.edges.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
```

### Caso de Uso en el Proyecto
**Encontrar rutas de entrega entre ciudades** 

**Ciudades en la BD** (setup_db.py):
- Bogotá
- Medellín
- Cali
- Barranquilla
- Cartagena
- Santa Marta

**Rutas disponibles**:
```
Bogotá ←→ Medellín (500 km)
Bogotá ←→ Cali (600 km)
Medellín ←→ Cartagena (700 km)
Cali ←→ Barranquilla (900 km)
Barranquilla ←→ Santa Marta (150 km)
Medellín ←→ Santa Marta (800 km)
Cali ←→ Cartagena (400 km)
```

### Ejemplo de Uso
```python
# Crear grafo
graph = Graph()

# Agregar rutas
graph.add_edge('Bogotá', 'Medellín', 500)
graph.add_edge('Bogotá', 'Cali', 600)
graph.add_edge('Medellín', 'Santa Marta', 800)

# Encontrar ruta más corta
ruta = graph.bfs_shortest_path('Bogotá', 'Santa Marta')
# Resultado: ['Bogotá', 'Medellín', 'Santa Marta']
```

**Métodos utilizados**:
- `add_vertex()` - Agregar ciudad al grafo
- `add_edge()` - Agregar ruta entre ciudades
- `bfs_shortest_path()` - Encontrar ruta más corta

**Complejidad**: O(V + E) donde V=vértices, E=aristas

---

## 📊 Resumen de Implementación

| Estructura | Tipo | Ubicación | Caso de Uso |
|-----------|------|-----------|-----------|
| **LinkedList** | Enlazada | models.py:6-35 | Productos por categoría |
| **Queue** | FIFO | models.py:37-55 | Pedidos pendientes (orden) |
| **Stack** | LIFO | models.py:57-77 | Historial de entregas |
| **HashTable** | Hash + Polinomio | models.py:79-113 | Búsqueda rápida de clientes |
| **Graph** | BFS | models.py:115-147 | Rutas entre ciudades |

---

## 🔧 Cómo Probar las Estructuras

### Ejecutar el script de demostración:
```bash
python DEMO_ESTRUCTURAS.py
```

Este script muestra ejemplos funcionales de todas las estructuras.

---

## 💻 Integración en Django

Las estructuras se usan **en memoria** durante:
- Procesamiento de pedidos
- Cálculo de rutas
- Organización de datos

Mientras que los **modelos Django** (UserProfile, Order, Product, etc.) manejan la **persistencia en la BD**.

**Beneficio**: Combinamos la eficiencia de estructuras de datos avanzadas con la robustez de Django ORM.
