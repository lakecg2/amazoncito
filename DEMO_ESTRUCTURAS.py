"""
DEMOSTRACIÓN DE ESTRUCTURAS DE DATOS - Amazoncito

Este archivo muestra cómo se utilizan las estructuras de datos
en el sistema de gestión de paqueterías.
"""

# =====================================================
# 1. LISTA ENLAZADA - Gestión de Categorías
# =====================================================

from amazoncito.models import LinkedList, Category, Product

# Crear una lista enlazada de categorías
categories_list = LinkedList()

# Agregar categorías
categories = ['Documentos', 'Paquetes', 'Electrónica', 'Ropa', 'Alimentos']
for category in categories:
    categories_list.append(category)

# Convertir a lista
print("CATEGORÍAS (Lista Enlazada):")
print(categories_list.to_list())
print()


# =====================================================
# 2. COLA - Procesamiento de Pedidos FIFO
# =====================================================

from amazoncito.models import Queue
from datetime import datetime

orders_queue = Queue()

# Agregar pedidos en orden de llegada
orders_data = [
    {'tracking': 'TRK001', 'customer': 'Cliente 1', 'city': 'Bogotá'},
    {'tracking': 'TRK002', 'customer': 'Cliente 2', 'city': 'Medellín'},
    {'tracking': 'TRK003', 'customer': 'Cliente 3', 'city': 'Cali'},
]

for order in orders_data:
    orders_queue.enqueue(order)

print("COLA DE PEDIDOS (FIFO):")
print(f"Tamaño de cola: {orders_queue.size()}")
print("Procesar primer pedido:")
first_order = orders_queue.dequeue()
print(f"  {first_order}")
print(f"Tamaño restante: {orders_queue.size()}")
print()


# =====================================================
# 3. PILA - Historial de Entregas LIFO
# =====================================================

from amazoncito.models import Stack

deliveries_stack = Stack()

# Agregar entregas completadas
completadas = [
    {'order': 'TRK001', 'date': '2024-11-20', 'customer': 'Cliente 1'},
    {'order': 'TRK002', 'date': '2024-11-21', 'customer': 'Cliente 2'},
    {'order': 'TRK003', 'date': '2024-11-22', 'customer': 'Cliente 3'},
]

for delivery in completadas:
    deliveries_stack.push(delivery)

print("PILA DE ENTREGAS (LIFO):")
print("Última entrega completada:")
last_delivery = deliveries_stack.peek()
print(f"  {last_delivery}")
print()


# =====================================================
# 4. TABLA HASH - Búsqueda de Clientes
# =====================================================

from amazoncito.models import HashTable

clients_hash = HashTable(size=100)

# Agregar clientes
clients = {
    'juan_perez': {'id': 1, 'name': 'Juan Pérez', 'city': 'Bogotá'},
    'maria_garcia': {'id': 2, 'name': 'María García', 'city': 'Medellín'},
    'carlos_sote': {'id': 3, 'name': 'Carlos Sote', 'city': 'Cali'},
}

print("TABLA HASH - Búsqueda de Clientes:")
for username, client_data in clients.items():
    clients_hash.insert(username, client_data)
    print(f"  ✓ {username} insertado en hash")

# Buscar un cliente
client = clients_hash.search('maria_garcia')
print(f"\nBúsqueda: maria_garcia")
print(f"  Resultado: {client}")
print()


# =====================================================
# 5. GRAFO - Rutas de Entrega
# =====================================================

from amazoncito.models import Graph

# Crear grafo de ciudades
delivery_graph = Graph()

# Agregar ciudades (vértices) - Colombia, México y Estados Unidos
cities = [
    # Colombia
    'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Santa Marta',
    # México
    'Ciudad de México', 'Monterrey', 'Guadalajara', 'Cancún',
    # Estados Unidos
    'Miami', 'Houston', 'Los Ángeles', 'Nueva York',
]

for city in cities:
    delivery_graph.add_vertex(city)

# Agregar rutas (aristas) - Red internacional
routes = [
    # Rutas internas Colombia
    ('Bogotá', 'Medellín', 500),
    ('Medellín', 'Cartagena', 700),
    ('Cartagena', 'Santa Marta', 150),
    
    # Rutas Colombia - México
    ('Bogotá', 'Ciudad de México', 2100),
    ('Cartagena', 'Cancún', 1800),
    
    # Rutas internas México
    ('Ciudad de México', 'Monterrey', 900),
    ('Monterrey', 'Guadalajara', 1200),
    ('Cancún', 'Ciudad de México', 1600),
    
    # Rutas México - Estados Unidos
    ('Monterrey', 'Houston', 800),
    ('Cancún', 'Miami', 300),
    ('Guadalajara', 'Los Ángeles', 2100),
    
    # Rutas internas Estados Unidos
    ('Houston', 'Miami', 1600),
    ('Houston', 'Nueva York', 2400),
    ('Miami', 'Nueva York', 1600),
    ('Los Ángeles', 'Nueva York', 4000),
    
    # Rutas directas internacionales
    ('Cartagena', 'Miami', 1200),
    ('Bogotá', 'Miami', 2000),
]

print("GRAFO - Red Internacional de Ciudades:")
for from_city, to_city, distance in routes:
    delivery_graph.add_edge(from_city, to_city, distance)
    print(f"  ✓ Ruta: {from_city:20} → {to_city:20} ({distance} km)")

# Encontrar rutas más cortas (BFS) - Ejemplos internacionales
print("\n" + "=" * 80)
print("RUTAS MÁS CORTAS (BFS) - Ejemplos Internacionales:")
print("=" * 80)

test_routes = [
    ('Bogotá', 'Miami'),
    ('Bogotá', 'Houston'),
    ('Cartagena', 'Nueva York'),
    ('Ciudad de México', 'Miami'),
    ('Medellín', 'Los Ángeles'),
]

for start, end in test_routes:
    shortest_path = delivery_graph.bfs_shortest_path(start, end)
    print(f"\n🗺️  De {start} a {end}:")
    if shortest_path:
        print(f"  Ruta: {' → '.join(shortest_path)}")
        print(f"  Paradas intermedias: {len(shortest_path) - 1}")
    else:
        print(f"  ⚠️  No hay ruta disponible")


# =====================================================
# RESUMEN DE COMPLEJIDADES
# =====================================================

print("=" * 60)
print("RESUMEN DE COMPLEJIDADES COMPUTACIONALES")
print("=" * 60)

complexities = {
    'LinkedList': {
        'append': 'O(n)',
        'search': 'O(n)',
    },
    'Queue': {
        'enqueue': 'O(1)',
        'dequeue': 'O(1)',
    },
    'Stack': {
        'push': 'O(1)',
        'pop': 'O(1)',
    },
    'HashTable': {
        'insert': 'O(1) avg',
        'search': 'O(1) avg',
    },
    'Graph (BFS)': {
        'buscar_ruta': 'O(V + E)',
    }
}

for structure, operations in complexities.items():
    print(f"\n{structure}:")
    for op, complexity in operations.items():
        print(f"  • {op}: {complexity}")


# =====================================================
# CASOS DE USO EN EL SISTEMA
# =====================================================

print("\n" + "=" * 60)
print("CASOS DE USO EN AMAZONCITO")
print("=" * 60)

use_cases = {
    '📦 Lista Enlazada': 'Mostrar productos por categoría en el dashboard',
    '⏳ Cola': 'Procesar pedidos pendientes en orden FIFO (primero en llegar)',
    '📚 Pila': 'Guardar historial de entregas completadas (último agregado)',
    '🔍 Hash': 'Buscar clientes rápidamente por username (O(1))',
    '🗺️ Grafo': 'Calcular ruta más corta entre ciudades para entregas',
}

for structure, use_case in use_cases.items():
    print(f"\n{structure}")
    print(f"  → {use_case}")

print("\n" + "=" * 60)
print("✅ TODAS LAS ESTRUCTURAS IMPLEMENTADAS Y INTEGRADAS")
print("=" * 60)
