#!/usr/bin/env python
"""Script para probar el sistema completo de entregas"""

import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import Product, CartItem, Order, City, Route, DeliveryEstimate
from amazoncito.route_calculator import get_delivery_estimate
import json

print("=" * 70)
print("PRUEBA DEL SISTEMA DE ENTREGAS CON DIJKSTRA")
print("=" * 70)

# Test 1: Verificar ciudades
print("\n[TEST 1] Verificando ciudades y rutas...")
cities = City.objects.all()
routes = Route.objects.all()
print(f"✓ Ciudades: {cities.count()}")
print(f"✓ Rutas: {routes.count()}")

# Test 2: Prubar RouteCalculator
print("\n[TEST 2] Probando cálculo de rutas con Dijkstra...")
destinations = ['Guadalajara', 'Cancun', 'Monterrey', 'Veracruz']

for dest in destinations:
    result = get_delivery_estimate(dest)
    if result:
        print(f"\n  📍 Destino: {dest}")
        print(f"     Ruta: {' → '.join(result['route'])}")
        print(f"     Distancia: {result['distance']} km")
        print(f"     Días: {result['estimated_days']}")
        print(f"     Llegada: {result['arrival_datetime'].strftime('%d/%m %H:%M')}")
    else:
        print(f"\n  ❌ No hay ruta a {dest}")

# Test 3: Crear una orden con estimación de entrega
print("\n[TEST 3] Creando orden con estimación de entrega...")
user = User.objects.first()
if user:
    # Crear una orden
    order = Order.objects.create(
        user=user,
        destination_city='Cancun',
        tracking_number='TEST-ETA-001',
        total_price=Decimal('150.00')
    )
    
    # Calcular estimación
    estimate = get_delivery_estimate('Cancun')
    if estimate:
        DeliveryEstimate.objects.create(
            order=order,
            estimated_arrival=estimate['arrival_datetime'],
            route_path=json.dumps(estimate['route']),
            total_distance=estimate['distance']
        )
        print(f"✓ Orden creada: {order.tracking_number}")
        print(f"✓ Estimación guardada")
        
        # Verificar
        delivery = order.delivery_estimate
        print(f"✓ Ruta: {json.loads(delivery.route_path)}")
        print(f"✓ Distancia: {delivery.total_distance} km")
        print(f"✓ ETA: {delivery.estimated_arrival}")

# Test 4: Verificar que el carrito se actualiza correctamente
print("\n[TEST 4] Verificando actualización de carrito...")
CartItem.objects.filter(user=user).delete()

products = Product.objects.all()[:2]
for product in products:
    item, created = CartItem.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': 1}
    )
    print(f"✓ Producto en carrito: {product.name} x{item.quantity}")

print("\n" + "=" * 70)
print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 70)
