"""
Script para inicializar las ciudades y rutas de entrega
Ejecutar con: python manage.py shell < initialize_routes.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
django.setup()

from amazoncito.models import City, Route

def initialize_cities_and_routes():
    """Inicializa ciudades principales de México y rutas entre ellas"""
    
    # Ciudades principales
    cities_data = [
        'Ciudad de Mexico',
        'Guadalajara',
        'Monterrey',
        'Cancun',
        'Merida',
        'Puebla',
        'Veracruz',
        'Querétaro',
        'San Luis Potosí',
        'Toluca',
    ]
    
    # Crear ciudades
    cities = {}
    for city_name in cities_data:
        city, created = City.objects.get_or_create(name=city_name)
        cities[city_name] = city
        if created:
            print(f"✓ Ciudad creada: {city_name}")
        else:
            print(f"• Ciudad existente: {city_name}")
    
    # Rutas con distancias aproximadas (en km) y días estimados
    routes_data = [
        # Desde CDMX
        ('Ciudad de Mexico', 'Guadalajara', 500, 1),
        ('Ciudad de Mexico', 'Monterrey', 900, 2),
        ('Ciudad de Mexico', 'Querétaro', 220, 1),
        ('Ciudad de Mexico', 'Toluca', 70, 1),
        ('Ciudad de Mexico', 'Puebla', 130, 1),
        
        # Rutas intermedias
        ('Guadalajara', 'Monterrey', 1000, 2),
        ('Querétaro', 'Monterrey', 680, 1),
        ('Puebla', 'Veracruz', 300, 1),
        ('Toluca', 'Puebla', 200, 1),
        
        # Hacia la península
        ('Puebla', 'Merida', 800, 2),
        ('Merida', 'Cancun', 320, 1),
        ('Ciudad de Mexico', 'Cancun', 1500, 2),
        
        # Alternativas
        ('Querétaro', 'San Luis Potosí', 360, 1),
        ('San Luis Potosí', 'Monterrey', 410, 1),
        ('Toluca', 'Guadalajara', 580, 1),
        ('Veracruz', 'Cancun', 1100, 2),
    ]
    
    # Crear rutas (bidireccionales)
    for from_city, to_city, distance, days in routes_data:
        # Ruta de ida
        route, created = Route.objects.get_or_create(
            from_city=cities[from_city],
            to_city=cities[to_city],
            defaults={'distance': distance, 'estimated_days': days}
        )
        if created:
            print(f"✓ Ruta creada: {from_city} → {to_city} ({distance} km, {days} día(s))")
        
        # Ruta de regreso (inversa)
        route_back, created = Route.objects.get_or_create(
            from_city=cities[to_city],
            to_city=cities[from_city],
            defaults={'distance': distance, 'estimated_days': days}
        )
        if created:
            print(f"✓ Ruta creada: {to_city} → {from_city} ({distance} km, {days} día(s))")
    
    print("\n✅ Inicialización completada!")

if __name__ == '__main__':
    initialize_cities_and_routes()
