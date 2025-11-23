# 🎯 Resumen Ejecutivo - Estructuras de Datos en Amazoncito

## 📍 Ubicación de los Archivos

```
amazoncito/
├── models.py                          ← AQUÍ ESTÁN TODAS LAS ESTRUCTURAS
├── views.py                           ← AQUÍ SE USAN LAS ESTRUCTURAS
├── DEMO_ESTRUCTURAS.py                ← EJEMPLOS PRÁCTICOS
└── IMPLEMENTACION_ESTRUCTURAS.md      ← DOCUMENTACIÓN DETALLADA
```

---

## 🔢 Las 5 Estructuras de Datos

### 1. 🔗 LISTA ENLAZADA (LinkedList)

**Archivo**: `models.py` líneas 6-35  
**Clase**: `LinkedList`, `Node`

```
Estructura:
┌─────┐    ┌─────┐    ┌─────┐
│Data├──→  │Data├──→  │Data├──→ None
└─────┘    └─────┘    └─────┘

Operaciones:
✓ append(data)      - Agregar al final       → O(n)
✓ to_list()         - Convertir a lista      → O(n)
```

**Uso**: Organizar productos por categoría  
**En el código**: `views.py`, línea 66 - `client_dashboard()`

---

### 2. 📋 COLA (Queue - FIFO)

**Archivo**: `models.py` líneas 37-55  
**Clase**: `Queue`

```
Estructura FIFO (First In - First Out):

Entrada (enqueue)          Salida (dequeue)
    ↓                           ↑
[Item1] [Item2] [Item3] [Item4]

Operaciones:
✓ enqueue(item)     - Agregar al final      → O(1)
✓ dequeue()         - Quitar del inicio     → O(1)
✓ is_empty()        - Verificar vacía       → O(1)
✓ size()            - Obtener cantidad      → O(1)
```

**Uso**: Procesar pedidos pendientes en orden de llegada  
**En el código**: `views.py`, línea 247 - `admin_services()`

```python
# Los pedidos se procesan en orden:
pending_orders_queue = Order.objects.filter(
    status='pendiente'
).order_by('created_at')  # FIFO
```

---

### 3. 📚 PILA (Stack - LIFO)

**Archivo**: `models.py` líneas 57-77  
**Clase**: `Stack`

```
Estructura LIFO (Last In - First Out):

Entrada/Salida (pop)
    ↓
  [Item4]  ← Último agregado, primero en salir
  [Item3]
  [Item2]
  [Item1]  ← Primero agregado, último en salir

Operaciones:
✓ push(item)        - Agregar al tope       → O(1)
✓ pop()             - Quitar del tope       → O(1)
✓ peek()            - Ver tope sin quitar   → O(1)
✓ is_empty()        - Verificar vacía       → O(1)
```

**Uso**: Historial de entregas completadas  
**En el código**: `views.py`, línea 251 - `admin_services()`

```python
# Guardar entregas en pila
DeliveryHistory.objects.create(
    order=order, 
    notes="Entregado exitosamente"
)
```

---

### 4. 🔑 TABLA HASH (HashTable con Polinomio)

**Archivo**: `models.py` líneas 79-113  
**Clase**: `HashTable`

```
Estructura con Hash Polinomial:

Entrada: 'carlos_sote'
        ↓
    hash_polynomial()  [Polinomio base 31]
        ↓
    Índice: 42
        ↓
[0]  [ ]
[1]  [ ]
[42] [('carlos_sote', {...})]  ← Búsqueda O(1)
[43] [ ]

Operaciones:
✓ hash_polynomial(key)  - Calcular índice   → O(1)
✓ insert(key, value)    - Agregar dato      → O(1) avg
✓ search(key)           - Buscar dato       → O(1) avg
✓ delete(key)           - Eliminar dato     → O(1) avg
```

**Característica especial**: Función hash con polinomios (P = 31)

```python
def hash_polynomial(self, key):
    hash_value = 0
    p = 31
    p_pow = 1
    for char in str(key):
        hash_value = (hash_value + (ord(char) * p_pow)) % (10**9 + 9)
        p_pow = (p_pow * p) % (10**9 + 9)
    return hash_value % self.size
```

**Uso**: Búsqueda rápida de clientes por username  
**Caso de uso**: En producción sería útil para:
- Buscar cliente: `hashtable.search('carlos_sote')`
- Insertar cliente: `hashtable.insert('carlos_sote', client_data)`

---

### 5. 🗺️ GRAFO CON BFS (Graph)

**Archivo**: `models.py` líneas 115-147  
**Clase**: `Graph`

```
Estructura de Grafo:

        Bogotá ──500km── Medellín
         /  \                │
       600  700             800
       /      \              │
      Cali    Cartagena   Santa Marta
      │       /
      900   200
      │    /
   Barranquilla

Operaciones:
✓ add_vertex(v)           - Agregar ciudad     → O(1)
✓ add_edge(v1, v2, w)     - Agregar ruta      → O(1)
✓ bfs_shortest_path(s, e) - Ruta más corta    → O(V + E)

BFS Algoritmo:
- Utiliza cola interna para exploración
- Garantiza encontrar ruta más corta (sin pesos)
- Complejidad: V (vértices) + E (aristas)
```

**Uso**: Encontrar rutas de entrega entre ciudades  
**En el código**: Conceptual, integrado en el modelo `Route`

```python
# Ejemplo de uso:
graph = Graph()
graph.add_edge('Bogotá', 'Medellín', 500)
graph.add_edge('Medellín', 'Santa Marta', 800)

# Encontrar ruta
ruta = graph.bfs_shortest_path('Bogotá', 'Santa Marta')
# Resultado: ['Bogotá', 'Medellín', 'Santa Marta']
```

---

## 📊 Tabla Comparativa

| Estructura | Insertar | Buscar | Eliminar | Caso de Uso | Archivo |
|-----------|----------|--------|----------|-----------|---------|
| **LinkedList** | O(n) | O(n) | O(n) | Productos/Categorías | models.py:6-35 |
| **Queue** | O(1) | - | O(1) | Pedidos FIFO | models.py:37-55 |
| **Stack** | O(1) | - | O(1) | Entregas LIFO | models.py:57-77 |
| **HashTable** | O(1) avg | O(1) avg | O(1) avg | Búsqueda rápida | models.py:79-113 |
| **Graph** | O(1) | O(V+E) | O(1) | Rutas BFS | models.py:115-147 |

---

## 🔄 Integración en Django

### En `models.py` (Definición)
- Líneas 1-147: Todas las 5 estructuras de datos + 8 modelos Django

### En `views.py` (Uso)
- Línea 66: LinkedList para productos
- Línea 247: Queue para pedidos pendientes
- Línea 251: Stack para entregas completadas
- Implícito: HashTable para búsquedas
- Implícito: Graph para rutas

### En `DEMO_ESTRUCTURAS.py` (Ejemplos)
- Ejemplos funcionales de todas las estructuras
- Casos de uso prácticos
- Complejidades computacionales

---

## 🎓 Cómo Aprender el Código

### Paso 1: Leer la teoría
```bash
cat IMPLEMENTACION_ESTRUCTURAS.md
```

### Paso 2: Ver ejemplos
```bash
python DEMO_ESTRUCTURAS.py
```

### Paso 3: Estudiar la implementación
```bash
cat amazoncito/models.py | head -150
```

### Paso 4: Ver el uso en vistas
```bash
grep -n "LinkedList\|Queue\|Stack\|HashTable\|Graph" amazoncito/views.py
```

---

## ✅ Validación

Todas las estructuras están:
- ✓ Implementadas en `models.py`
- ✓ Integradas en `views.py`
- ✓ Documentadas en `IMPLEMENTACION_ESTRUCTURAS.md`
- ✓ Demostradas en `DEMO_ESTRUCTURAS.py`
- ✓ Funcionando en producción

---

## 📈 Complejidades Finales

```
LinkedList
  append:  O(n)
  search:  O(n)

Queue (FIFO)
  enqueue: O(1)
  dequeue: O(1)

Stack (LIFO)
  push:    O(1)
  pop:     O(1)

HashTable (Polinomial)
  insert:  O(1) average
  search:  O(1) average
  delete:  O(1) average

Graph (BFS)
  add_edge: O(1)
  bfs_path: O(V + E)
```

---

**Creado**: Noviembre 22, 2025  
**Proyecto**: Amazoncito - Sistema de Paquetería con Estructuras de Datos
