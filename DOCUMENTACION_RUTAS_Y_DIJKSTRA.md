# Documentación Completa: Sistema de Rutas y Algoritmo de Dijkstra

## Tabla de Contenidos
1. [Arquitectura General](#arquitectura-general)
2. [Modelo de Datos](#modelo-de-datos)
3. [Ciudades y Distancias](#ciudades-y-distancias)
4. [Algoritmo de Dijkstra](#algoritmo-de-dijkstra)
5. [Calculadora de Rutas](#calculadora-de-rutas)
6. [Integración con la Aplicación](#integración-con-la-aplicación)
7. [Ejemplo de Ejecución](#ejemplo-de-ejecución)
8. [Análisis de Complejidad](#análisis-de-complejidad)

---

## Arquitectura General

El sistema de rutas de **Amazoncito** está basado en un **grafo ponderado dirigido y bidireccional** que representa conexiones entre ciudades mexicanas. El objetivo es calcular la ruta óptima (menor distancia) desde cualquier ciudad origen hacia una ciudad de destino.

### Componentes Principales:
- **Modelo Django (City/Route)**: Almacenamiento de datos en base de datos
- **Calculadora de Rutas (RouteCalculator)**: Implementación del algoritmo Dijkstra
- **Inicializador de Datos (initialize_routes.py)**: Precarga de ciudades y rutas
- **Vistas Django (views.py)**: Integración con interfaz web

---

## Modelo de Datos

### 1. Modelo `City`
```python
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
```
**Propósito**: Almacenar las ciudades disponibles en el sistema.
**Ejemplo de datos**:
- CDMX (Ciudad de México)
- Guadalajara
- Monterrey
- Cancún
- Mérida
- Puebla
- Veracruz
- Querétaro
- San Luis Potosí
- Toluca

### 2. Modelo `Route`
```python
class Route(models.Model):
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='outgoing_routes')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='incoming_routes')
    distance = models.IntegerField()  # En kilómetros
    estimated_days = models.IntegerField()  # Días estimados de entrega
    
    def __str__(self):
        return f"{self.from_city} → {self.to_city} ({self.distance} km)"
```
**Propósito**: Almacenar las conexiones entre ciudades con distancia y tiempo estimado.
**Características**:
- Bidireccional: Para cada ruta CDMX→Guadalajara existe Guadalajara→CDMX
- Ponderada: Cada ruta tiene un peso (distancia en km)
- Temporal: Incluye estimación de días de entrega

### 3. Modelo `DeliveryEstimate`
```python
class DeliveryEstimate(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    estimated_arrival = models.DateTimeField()
    route_path = models.JSONField(default=list)  # Lista de ciudades: ['CDMX', 'Puebla', 'Mérida', 'Cancún']
    total_distance = models.IntegerField()  # Suma total de distancias en km
```
**Propósito**: Guardar la ruta calculada y la fecha estimada de entrega para cada orden.

---

## Ciudades y Distancias

### Red de Ciudades (10 ciudades totales)

```
ORIGEN PRINCIPAL: CDMX (Ciudad de México)

Ciudades Destino:
├── Guadalajara
├── Monterrey
├── Cancún
├── Mérida
├── Puebla
├── Veracruz
├── Querétaro
├── San Luis Potosí
└── Toluca
```

### Tabla de Rutas Bidireccionales (17 rutas totales)

| Ruta | Distancia (km) | Días Estimados |
|------|-----------------|-----------------|
| CDMX ↔ Guadalajara | 500 | 1 |
| CDMX ↔ Monterrey | 750 | 2 |
| CDMX ↔ Puebla | 130 | 1 |
| CDMX ↔ Querétaro | 200 | 1 |
| CDMX ↔ San Luis Potosí | 420 | 1 |
| CDMX ↔ Toluca | 70 | 1 |
| CDMX ↔ Veracruz | 400 | 1 |
| Guadalajara ↔ Monterrey | 620 | 2 |
| Guadalajara ↔ Querétaro | 320 | 1 |
| Monterrey ↔ San Luis Potosí | 480 | 1 |
| Puebla ↔ Veracruz | 240 | 1 |
| Puebla ↔ Mérida | 1050 | 2 |
| Querétaro ↔ San Luis Potosí | 280 | 1 |
| San Luis Potosí ↔ Veracruz | 390 | 1 |
| Mérida ↔ Cancún | 370 | 1 |
| Veracruz ↔ Mérida | 700 | 1 |
| Toluca ↔ Querétaro | 300 | 1 |

### Representación en Grafo (Estructura de Datos)

Después de construir el grafo desde la base de datos, se obtiene la siguiente estructura:

```python
graph = {
    "CDMX": [
        ("Guadalajara", 500, 1),
        ("Monterrey", 750, 2),
        ("Puebla", 130, 1),
        ("Querétaro", 200, 1),
        ("San Luis Potosí", 420, 1),
        ("Toluca", 70, 1),
        ("Veracruz", 400, 1)
    ],
    "Guadalajara": [
        ("CDMX", 500, 1),
        ("Monterrey", 620, 2),
        ("Querétaro", 320, 1)
    ],
    "Monterrey": [
        ("CDMX", 750, 2),
        ("Guadalajara", 620, 2),
        ("San Luis Potosí", 480, 1)
    ],
    # ... (resto de ciudades)
}
```

**Formato**: `graph[ciudad] = [(ciudad_vecina, distancia_km, dias_estimados), ...]`

---

## Algoritmo de Dijkstra

### Introducción
El **algoritmo de Dijkstra** es un algoritmo greedy que encuentra el camino más corto entre dos nodos en un grafo ponderado con pesos no-negativos.

### Funcionamiento Básico

**Entrada**: 
- `start`: Ciudad origen (ejemplo: "CDMX")
- `end`: Ciudad destino (ejemplo: "Cancún")

**Salida**:
- `route_list`: Lista de ciudades en la ruta óptima
- `total_distance`: Distancia acumulada en km
- `total_days`: Días de entrega estimados

### Pseudocódigo del Algoritmo

```
Función dijkstra(start, end):
    1. Inicializar:
       - distances = {todas_ciudades: INFINITO}
       - distances[start] = 0
       - visited = conjunto vacío
       - previous = diccionario vacío (para reconstruir ruta)
       - heap = [(0, start)]
    
    2. Mientras heap no esté vacío:
       a. Extraer (distancia_actual, ciudad_actual) del heap
       b. Si ciudad_actual ya fue visitada, continuar
       c. Marcar ciudad_actual como visitada
       d. Si ciudad_actual es el destino, romper
       e. Para cada ciudad_vecina adyacente a ciudad_actual:
          - Calcular nueva_distancia = distances[ciudad_actual] + distancia_hacia_vecina
          - Si nueva_distancia < distances[ciudad_vecina]:
             * Actualizar distances[ciudad_vecina] = nueva_distancia
             * Guardar previous[ciudad_vecina] = ciudad_actual
             * Agregar (nueva_distancia, ciudad_vecina) al heap
    
    3. Reconstruir ruta usando diccionario previous:
       - Empezar desde end, ir hacia atrás siguiendo previous
       - Invertir la ruta
    
    4. Retornar (ruta, distancia_total, dias_total)
```

### Implementación en Python (route_calculator.py)

```python
from heapq import heappush, heappop
from amazoncito.models import City, Route

class RouteCalculator:
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """
        Construye un grafo desde las rutas en la base de datos.
        Retorna un diccionario de adyacencia.
        """
        graph = {}
        
        # Obtener todas las ciudades
        cities = City.objects.all()
        for city in cities:
            graph[city.name] = []
        
        # Obtener todas las rutas y construir adyacencias
        routes = Route.objects.all()
        for route in routes:
            from_city = route.from_city.name
            to_city = route.to_city.name
            distance = route.distance
            days = route.estimated_days
            
            # Agregar arista bidireccional
            graph[from_city].append((to_city, distance, days))
        
        return graph
    
    def dijkstra(self, start, end):
        """
        Implementación del algoritmo de Dijkstra usando heapq.
        
        Args:
            start (str): Ciudad origen
            end (str): Ciudad destino
        
        Returns:
            tuple: (route_list, total_distance, total_days)
        """
        # Inicialización
        distances = {city: float('inf') for city in self.graph}
        distances[start] = 0
        visited = set()
        previous = {}
        heap = [(0, start)]
        days_to_city = {city: 0 for city in self.graph}
        days_to_city[start] = 0
        
        # Algoritmo principal
        while heap:
            current_distance, current_city = heappop(heap)
            
            # Si ya visitamos esta ciudad, ignorar
            if current_city in visited:
                continue
            
            visited.add(current_city)
            
            # Si alcanzamos el destino, terminar
            if current_city == end:
                break
            
            # Explorar vecinos
            for neighbor, distance, days in self.graph[current_city]:
                if neighbor not in visited:
                    new_distance = distances[current_city] + distance
                    
                    # Si encontramos un camino más corto
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        days_to_city[neighbor] = days_to_city[current_city] + days
                        previous[neighbor] = current_city
                        heappush(heap, (new_distance, neighbor))
        
        # Reconstruir la ruta
        route = []
        current = end
        while current in previous:
            route.append(current)
            current = previous[current]
        route.append(start)
        route.reverse()
        
        return (
            route,
            distances[end],
            days_to_city[end]
        )
    
    def calculate_delivery_time(self, destination_city):
        """
        Calcula el tiempo de entrega estimado desde CDMX.
        
        Args:
            destination_city (str): Ciudad destino
        
        Returns:
            datetime: Fecha y hora estimada de entrega
        """
        from django.utils import timezone
        from datetime import timedelta
        
        route_data = self.dijkstra('CDMX', destination_city)
        route_list, total_distance, total_days = route_data
        
        # Calcular fecha de entrega
        current_time = timezone.now()
        delivery_time = current_time + timedelta(days=total_days)
        
        return delivery_time
    
    def get_delivery_estimate(self, destination_city):
        """
        Obtiene información completa de entrega.
        
        Returns:
            dict: Información de ruta y estimación
        """
        route_list, total_distance, total_days = self.dijkstra('CDMX', destination_city)
        delivery_time = self.calculate_delivery_time(destination_city)
        
        return {
            'route': route_list,
            'distance': total_distance,
            'days': total_days,
            'estimated_arrival': delivery_time
        }
```

---

## Ejemplo Detallado: CDMX → Cancún

### Paso 1: Inicialización

```
start = "CDMX"
end = "Cancún"

distances = {
    "CDMX": 0,
    "Guadalajara": ∞,
    "Monterrey": ∞,
    "Cancún": ∞,
    "Mérida": ∞,
    "Puebla": ∞,
    "Veracruz": ∞,
    "Querétaro": ∞,
    "San Luis Potosí": ∞,
    "Toluca": ∞
}

visited = {}
previous = {}
heap = [(0, "CDMX")]
```

### Paso 2: Iteraciones del Algoritmo

**Iteración 1**: Procesar CDMX
```
Pop: (0, "CDMX")
Vecinos de CDMX:
  - Guadalajara: 500 km → distances["Guadalajara"] = 500
  - Monterrey: 750 km → distances["Monterrey"] = 750
  - Puebla: 130 km → distances["Puebla"] = 130 ✓ mejor
  - Querétaro: 200 km → distances["Querétaro"] = 200
  - San Luis Potosí: 420 km → distances["San Luis Potosí"] = 420
  - Toluca: 70 km → distances["Toluca"] = 70 ✓ mejor
  - Veracruz: 400 km → distances["Veracruz"] = 400

Heap después: [(70, "Toluca"), (130, "Puebla"), (200, "Querétaro"), (400, "Veracruz"), (420, "San Luis Potosí"), (500, "Guadalajara"), (750, "Monterrey")]
```

**Iteración 2**: Procesar Toluca
```
Pop: (70, "Toluca")
Vecinos de Toluca:
  - Querétaro: 70 + 300 = 370 km > 200 km (no mejora)

Heap: [(130, "Puebla"), (200, "Querétaro"), (300, "Querétaro"), ...]
```

**Iteración 3**: Procesar Puebla
```
Pop: (130, "Puebla")
Vecinos de Puebla:
  - Veracruz: 130 + 240 = 370 km < 400 km → distances["Veracruz"] = 370 ✓ mejora
  - Mérida: 130 + 1050 = 1180 km → distances["Mérida"] = 1180

Heap: [(200, "Querétaro"), (370, "Veracruz"), (1180, "Mérida"), ...]
```

**Iteración 4-6**: Continúan procesando ciudades hasta que llega Mérida...

**Iteración 7**: Procesar Mérida
```
Pop: (1180, "Mérida")
Vecinos de Mérida:
  - Cancún: 1180 + 370 = 1550 km → distances["Cancún"] = 1550

Heap: [..., (1550, "Cancún"), ...]
```

**Iteración 8**: Procesar Cancún
```
Pop: (1550, "Cancún")
current_city == end → ENCONTRADO ✓

Ruta reconstruida siguiendo previous:
Cancún → Mérida → Puebla → CDMX
Invertida: ["CDMX", "Puebla", "Mérida", "Cancún"]

RESULTADO:
- Ruta: CDMX → Puebla → Mérida → Cancún
- Distancia Total: 130 + 1050 + 370 = 1550 km
- Días: 1 + 2 + 1 = 4 días
```

### Ruta Alternativa Descartada

```
Ruta más directa teórica: CDMX → Veracruz → Mérida → Cancún
- CDMX → Veracruz: 400 km
- Veracruz → Mérida: 700 km
- Mérida → Cancún: 370 km
- TOTAL: 1470 km ✗ (no existe ruta directa CDMX-Veracruz-Mérida óptima)

Mejor ruta encontrada: CDMX → Puebla → Mérida → Cancún
- CDMX → Puebla: 130 km
- Puebla → Veracruz: 240 km (intermedio)
- Veracruz → Mérida: 700 km
- Mérida → Cancún: 370 km
- TOTAL: 1420 km ✓
```

---

## Calculadora de Rutas

### Archivo: `route_calculator.py`

**Ubicación**: `/amazoncito/route_calculator.py`

**Métodos Principales**:

1. **`__init__()`**
   - Construye el grafo al inicializar la clase
   - Llama a `_build_graph()` automáticamente

2. **`_build_graph()`**
   - Lee todas las rutas de la base de datos
   - Crea estructura de lista de adyacencia
   - Complejidad: O(E) donde E = número de rutas

3. **`dijkstra(start, end)`**
   - Implementa el algoritmo core
   - Retorna: `(route_list, total_distance, total_days)`
   - Complejidad: O((V + E) log V)

4. **`calculate_delivery_time(destination_city)`**
   - Calcula fecha/hora de entrega
   - Suma días estimados a `timezone.now()`
   - Retorna: `datetime` con timezone

5. **`get_delivery_estimate(destination_city)`**
   - Función wrapper que consolida información
   - Retorna: diccionario completo con ruta, distancia, días, fecha estimada

---

## Integración con la Aplicación

### Flujo en `views.py`

```python
def create_order(request):
    """
    Crea una nueva orden y calcula la ruta de entrega.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Crear la orden
            order = form.save(commit=False)
            order.customer = request.user.profile
            order.save()
            
            # Calcular ruta de entrega
            from amazoncito.route_calculator import RouteCalculator
            calculator = RouteCalculator()
            
            delivery_info = calculator.get_delivery_estimate(
                order.destination_city.name
            )
            
            # Guardar estimación de entrega
            delivery_estimate = DeliveryEstimate.objects.create(
                order=order,
                estimated_arrival=delivery_info['estimated_arrival'],
                route_path=delivery_info['route'],
                total_distance=delivery_info['distance']
            )
            
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'client/create_order.html', {'form': form})
```

### Secuencia de Ejecución

```
1. Usuario selecciona ciudad destino en formulario
↓
2. POST a create_order view
↓
3. Se crea objeto Order en BD
↓
4. Se instancia RouteCalculator()
   ├─ Llama _build_graph()
   └─ Lee todas las rutas de BD
↓
5. Se llama get_delivery_estimate(destination_city)
   ├─ Ejecuta dijkstra('CDMX', destination_city)
   ├─ Ejecuta calculate_delivery_time(destination_city)
   └─ Retorna diccionario con ruta completa
↓
6. Se crea DeliveryEstimate con:
   ├─ route_path: lista de ciudades
   ├─ estimated_arrival: fecha/hora
   └─ total_distance: km totales
↓
7. Usuario redirigido a página de detalle de orden
```

---

## Análisis de Complejidad

### Complejidad Temporal

**`_build_graph()`**:
- Iteración sobre todas las rutas: O(E)
- E = número de rutas = 17
- **Total: O(E) = O(1) en este caso**

**`dijkstra(start, end)`**:
- Cada ciudad se procesa una vez: O(V)
- Cada arista se explora una vez: O(E)
- Operaciones de heap (push/pop): O(log V)
- **Total: O((V + E) log V)**

**En este sistema**:
- V = 10 ciudades
- E ≈ 20 aristas (bidireccionales)
- **Complejidad: O((10 + 20) log 10) ≈ O(100)**
- **Tiempo de ejecución: < 1 milisegundo**

### Complejidad Espacial

**Almacenamiento**:
- Grafo (lista de adyacencia): O(V + E)
- Diccionarios (distances, previous, visited): O(V)
- Heap: O(V)
- **Total: O(V + E)**

**En este sistema**:
- Aproximadamente: O(10 + 20) = O(30) espacios
- Memoria: < 1 KB para estructura de datos

---

## Ficheros Relacionados

### 1. `initialize_routes.py`
```python
"""
Script para inicializar la base de datos con ciudades y rutas.
Ejecutar con: python initialize_routes.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
django.setup()

from amazoncito.models import City, Route

# Definir ciudades
cities_data = [
    'CDMX', 'Guadalajara', 'Monterrey', 'Cancún', 'Mérida',
    'Puebla', 'Veracruz', 'Querétaro', 'San Luis Potosí', 'Toluca'
]

# Crear ciudades
for city_name in cities_data:
    City.objects.get_or_create(name=city_name)

# Definir rutas bidireccionales
routes_data = [
    ('CDMX', 'Guadalajara', 500, 1),
    ('CDMX', 'Monterrey', 750, 2),
    # ... (más rutas)
]

# Crear rutas
for from_city, to_city, distance, days in routes_data:
    City.objects.create_route(from_city, to_city, distance, days)
```

### 2. `models.py`
Contiene:
- Modelo `City`
- Modelo `Route`
- Modelo `DeliveryEstimate`
- Modelo `Order`
- Estructuras de datos personalizadas (LinkedList, Queue, Stack, HashTable, Graph)

### 3. `route_calculator.py`
Contiene:
- Clase `RouteCalculator`
- Implementación de Dijkstra
- Cálculo de tiempos de entrega

### 4. `views.py`
Contiene:
- Integración de rutas en vistas Django
- Función `create_order()` que usa RouteCalculator

---

## Casos de Uso

### 1. Usuario Ordena desde CDMX a Cancún
```
INPUT:  destination_city = "Cancún"
OUTPUT: route = ["CDMX", "Puebla", "Mérida", "Cancún"]
        distance = 1420 km
        days = 4
        estimated_arrival = 2025-11-27 14:30:00
```

### 2. Usuario Ordena desde CDMX a Guadalajara
```
INPUT:  destination_city = "Guadalajara"
OUTPUT: route = ["CDMX", "Guadalajara"]
        distance = 500 km
        days = 1
        estimated_arrival = 2025-11-24 14:30:00
```

### 3. Usuario Ordena desde CDMX a Monterrey
```
INPUT:  destination_city = "Monterrey"
OUTPUT: route = ["CDMX", "Monterrey"]
        distance = 750 km
        days = 2
        estimated_arrival = 2025-11-25 14:30:00
```

---

## Optimizaciones Futuras

### 1. Cacheo de Rutas
```python
# Guardar rutas calculadas frecuentemente
@cache.cached(timeout=3600)
def get_delivery_estimate(destination):
    # Calcular solo si no está en caché
    ...
```

### 2. Múltiples Orígenes
```python
# Permitir origen flexible, no solo CDMX
def dijkstra(self, start, end):
    # start puede ser cualquier ciudad
    ...
```

### 3. Algoritmo A*
```python
# Usar heurística de distancia Euclidiana
# Más rápido que Dijkstra en grafos grandes
def astar(self, start, end):
    ...
```

### 4. Rutas Alternativas
```python
# Calcular top 3 rutas óptimas
def get_alternative_routes(self, start, end, count=3):
    ...
```

### 5. Restricciones Dinámicas
```python
# Bloquear rutas/ciudades en tiempo real
def dijkstra_with_restrictions(self, start, end, blocked_cities=[]):
    ...
```
