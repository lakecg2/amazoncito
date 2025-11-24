"""
Calculador de rutas óptimas usando algoritmo de Dijkstra
Para calcular la ruta más rápida desde CDMX a la ciudad de destino
"""

import heapq
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Optional
from .models import City, Route


class RouteCalculator:
    """Calcula la ruta óptima entre ciudades usando algoritmo de Dijkstra"""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self) -> Dict[str, List[Tuple[str, int, int]]]:
        """
        Construye un grafo con las rutas disponibles
        Retorna: {ciudad: [(ciudad_destino, distancia, dias_estimados), ...]}
        """
        graph = {}
        
        # Obtener todas las ciudades
        cities = City.objects.all()
        for city in cities:
            if city.name not in graph:
                graph[city.name] = []
        
        # Obtener todas las rutas
        routes = Route.objects.all()
        for route in routes:
            from_city = route.from_city.name
            to_city = route.to_city.name
            
            if from_city not in graph:
                graph[from_city] = []
            if to_city not in graph:
                graph[to_city] = []
            
            # Agregar ruta en ambas direcciones (grafo no dirigido)
            graph[from_city].append((to_city, route.distance, route.estimated_days))
            graph[to_city].append((from_city, route.distance, route.estimated_days))
        
        return graph
    
    def dijkstra(self, start: str, end: str) -> Optional[Tuple[List[str], int, int]]:
        """
        Implementa algoritmo de Dijkstra para encontrar la ruta más corta
        
        Args:
            start: Ciudad de origen
            end: Ciudad de destino
        
        Returns:
            (ruta, distancia_total, dias_totales) o None si no hay ruta
        """
        if start not in self.graph or end not in self.graph:
            return None
        
        # Distancias iniciales
        distances = {city: float('inf') for city in self.graph}
        distances[start] = 0
        
        # Para rastrear la ruta
        previous = {city: None for city in self.graph}
        
        # Cola de prioridad: (distancia, ciudad)
        heap = [(0, start)]
        
        # Para rastrear días de viaje
        total_days = {city: float('inf') for city in self.graph}
        total_days[start] = 0
        
        visited = set()
        
        while heap:
            current_distance, current_city = heapq.heappop(heap)
            
            if current_city in visited:
                continue
            
            visited.add(current_city)
            
            # Si llegamos al destino
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
        
        # Reconstruir la ruta
        if distances[end] == float('inf'):
            return None  # No hay ruta disponible
        
        route = []
        current = end
        while current is not None:
            route.append(current)
            current = previous[current]
        route.reverse()
        
        return (route, distances[end], total_days[end])
    
    def calculate_delivery_time(self, destination_city: str) -> Optional[Dict]:
        """
        Calcula el tiempo estimado de entrega desde CDMX
        
        Args:
            destination_city: Nombre de la ciudad destino
        
        Returns:
            {
                'arrival_datetime': datetime,
                'route': [ciudades],
                'distance': km,
                'estimated_days': dias
            } o None si no hay ruta
        """
        result = self.dijkstra('Ciudad de Mexico', destination_city)
        
        if result is None:
            return None
        
        route, distance, days = result
        
        # Calcular datetime de llegada (timezone-aware)
        now = datetime.now(timezone.utc)
        arrival = now + timedelta(days=int(days))
        
        return {
            'arrival_datetime': arrival,
            'route': route,
            'distance': distance,
            'estimated_days': int(days)
        }


# Función utilitaria
def get_delivery_estimate(destination_city: str) -> Optional[Dict]:
    """
    Obtiene estimación de entrega para una ciudad destino
    """
    calculator = RouteCalculator()
    return calculator.calculate_delivery_time(destination_city)
