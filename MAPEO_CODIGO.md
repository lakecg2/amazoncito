"""
MAPEO DE LÍNEAS - Estructuras de Datos en models.py
Ubicación exacta de cada estructura en el archivo
"""

📁 amazoncito/models.py (263 líneas totales)
│
├─ 📌 ESTRUCTURAS DE DATOS (Líneas 1-147)
│  │
│  ├─ 🔗 LISTA ENLAZADA (Líneas 6-35)
│  │  ├─ class Node(lines 6-9)
│  │  │  └─ __init__(data)
│  │  │
│  │  └─ class LinkedList(lines 11-35)
│  │     ├─ __init__()                      → Inicializar lista vacía
│  │     ├─ append(data)                    → Agregar nodo al final
│  │     └─ to_list()                       → Convertir a lista Python
│  │
│  ├─ 📋 COLA - FIFO (Líneas 37-55)
│  │  └─ class Queue(lines 37-55)
│  │     ├─ __init__()                      → Inicializar cola vacía
│  │     ├─ enqueue(item)                   → Agregar al final
│  │     ├─ dequeue()                       → Quitar del inicio
│  │     ├─ is_empty()                      → ¿Está vacía?
│  │     └─ size()                          → Contar elementos
│  │
│  ├─ 📚 PILA - LIFO (Líneas 57-77)
│  │  └─ class Stack(lines 57-77)
│  │     ├─ __init__()                      → Inicializar pila vacía
│  │     ├─ push(item)                      → Agregar al tope
│  │     ├─ pop()                           → Quitar del tope
│  │     ├─ is_empty()                      → ¿Está vacía?
│  │     └─ peek()                          → Ver tope sin quitar
│  │
│  ├─ 🔑 TABLA HASH (Líneas 79-113)
│  │  └─ class HashTable(lines 79-113)
│  │     ├─ __init__(size=100)              → Crear tabla con 100 buckets
│  │     ├─ hash_polynomial(key)            → Función hash con polinomio base 31
│  │     ├─ insert(key, value)              → Insertar con O(1)
│  │     ├─ search(key)                     → Buscar con O(1)
│  │     └─ delete(key)                     → Eliminar con O(1)
│  │
│  └─ 🗺️ GRAFO CON BFS (Líneas 115-147)
│     └─ class Graph(lines 115-147)
│        ├─ __init__()                      → Inicializar grafo vacío
│        ├─ add_vertex(vertex)              → Agregar ciudad
│        ├─ add_edge(v1, v2, weight)        → Agregar ruta
│        └─ bfs_shortest_path(start, end)   → Encontrar ruta más corta
│
│
├─ 🗄️ MODELOS DJANGO (Líneas 149-263)
│  │
│  ├─ 👤 UserProfile (Líneas 155-169)
│  │  └─ Perfil extendido de usuario
│  │     ├─ user (OneToOne → User)
│  │     ├─ role (cliente|admin)
│  │     ├─ description, address, phone
│  │     └─ created_at
│  │
│  ├─ 📦 Category (Líneas 171-179)
│  │  └─ Categoría de productos
│  │     ├─ name (único)
│  │     └─ description
│  │
│  ├─ 🛍️ Product (Líneas 181-191)
│  │  └─ Productos en el catálogo
│  │     ├─ category (FK → Category)
│  │     ├─ name, description
│  │     ├─ price (DecimalField)
│  │     └─ weight
│  │
│  ├─ 📋 Order (Líneas 193-207)
│  │  └─ Pedidos de clientes
│  │     ├─ user (FK → User)
│  │     ├─ products (M2M → Product)
│  │     ├─ status (pendiente|procesando|enviado|entregado|cancelado)
│  │     ├─ destination_city
│  │     ├─ tracking_number (único)
│  │     ├─ total_price, cancellation_message
│  │     └─ created_at, updated_at
│  │
│  ├─ 📌 OrderItem (Líneas 209-215)
│  │  └─ Items dentro de un pedido (M2M through)
│  │     ├─ order (FK)
│  │     ├─ product (FK)
│  │     ├─ quantity
│  │     └─ price
│  │
│  ├─ 🌍 City (Líneas 217-221)
│  │  └─ Ciudades para entregas
│  │     └─ name (único)
│  │
│  ├─ 🚚 Route (Líneas 223-231)
│  │  └─ Rutas entre ciudades
│  │     ├─ from_city (FK)
│  │     ├─ to_city (FK)
│  │     ├─ distance (km)
│  │     └─ estimated_days
│  │
│  ├─ 📚 DeliveryHistory (Líneas 233-240)
│  │  └─ Historial de entregas (implementación STACK)
│  │     ├─ order (FK)
│  │     ├─ delivered_at
│  │     └─ notes
│  │
│  └─ 🔔 NotificationMessage (Líneas 242-251)
│     └─ Mensajes de notificación
│        ├─ user (FK)
│        ├─ order (FK)
│        ├─ message
│        ├─ is_read
│        └─ created_at


📁 amazoncito/views.py (DONDE SE USAN LAS ESTRUCTURAS)
│
├─ 🔗 LinkedList (Línea ~66)
│  └─ En client_dashboard()
│     Organizar productos por categoría
│
├─ 📋 Queue (Línea ~247)
│  └─ En admin_services()
│     Procesar pedidos en orden FIFO
│
├─ 📚 Stack (Línea ~251)
│  └─ En admin_services()
│     Guardar entregas completadas
│
├─ 🔑 HashTable (Implícito)
│  └─ En búsquedas de clientes
│     Búsqueda O(1) por username
│
└─ 🗺️ Graph (Implícito)
   └─ En cálculo de rutas
      Encontrar camino más corto entre ciudades


📁 DEMO_ESTRUCTURAS.py
│
├─ Sección 1: Demostración LinkedList
├─ Sección 2: Demostración Queue
├─ Sección 3: Demostración Stack
├─ Sección 4: Demostración HashTable
├─ Sección 5: Demostración Graph + BFS
├─ Tabla de Complejidades
└─ Casos de Uso en Amazoncito


═══════════════════════════════════════════════════════════════════

CÓMO NAVEGAR EL CÓDIGO:

1. Para ver la IMPLEMENTACIÓN:
   → Abre: amazoncito/models.py
   → Lee: Líneas 1-147 (Estructuras de datos)

2. Para ver el CÓDIGO COMPLETO:
   → Abre: amazoncito/models.py
   → Lee: Líneas 1-263 (Estructuras + Modelos Django)

3. Para ver EJEMPLOS PRÁCTICOS:
   → Abre: DEMO_ESTRUCTURAS.py
   → Ejecuta: python DEMO_ESTRUCTURAS.py

4. Para ver DOCUMENTACIÓN DETALLADA:
   → Lee: IMPLEMENTACION_ESTRUCTURAS.md
   → Lee: RESUMEN_ESTRUCTURAS.md

5. Para ver USO EN VISTAS:
   → Abre: amazoncito/views.py
   → Busca: "pending_orders_queue", "DeliveryHistory", etc.

═══════════════════════════════════════════════════════════════════

COMPARATIVA DE UBICACIÓN:

┌──────────────────┬─────────────────────┬──────────────────────────┐
│   Estructura     │    Definida en      │     Usada en            │
├──────────────────┼─────────────────────┼──────────────────────────┤
│  LinkedList      │ models.py (6-35)    │ views.py:66             │
│  Queue           │ models.py (37-55)   │ views.py:247            │
│  Stack           │ models.py (57-77)   │ views.py:251 + modelo   │
│  HashTable       │ models.py (79-113)  │ Búsquedas implícitas   │
│  Graph           │ models.py (115-147) │ Rutas implícitas        │
└──────────────────┴─────────────────────┴──────────────────────────┘

═══════════════════════════════════════════════════════════════════
"""
