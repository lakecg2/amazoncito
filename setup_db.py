#!/usr/bin/env python
"""
Script para ejecutar las migraciones y configurar la base de datos.
Ejecutar después de crear el proyecto: python setup_db.py
"""
import os
import django
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
django.setup()

print("=" * 60)
print("CONFIGURANDO BASE DE DATOS - Amazoncito")
print("=" * 60)

# Crear migraciones
print("\n1. Creando migraciones...")
try:
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
    print("✅ Migraciones creadas exitosamente")
except Exception as e:
    print(f"⚠️ Error al crear migraciones: {e}")

# Ejecutar migraciones
print("\n2. Aplicando migraciones...")
try:
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    print("✅ Migraciones aplicadas exitosamente")
except Exception as e:
    print(f"⚠️ Error al aplicar migraciones: {e}")

# Crear superusuario admin
print("\n3. Creando administrador...")
from django.contrib.auth.models import User
from amazoncito.models import UserProfile

if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_user(username='admin', password='Amazoncito123', email='admin@amazoncito.local')
    UserProfile.objects.create(user=admin_user, role='admin')
    print("✅ Administrador creado: admin / Amazoncito123")
else:
    print("⚠️ El administrador ya existe")

# Crear datos de prueba
print("\n4. Cargando datos iniciales...")
from amazoncito.models import Category, Product, City, Route

# Categorías
categories_data = [
    {'name': 'Documentos', 'description': 'Documentos y papelería'},
    {'name': 'Paquetes', 'description': 'Cajas y empaques'},
    {'name': 'Electrónica', 'description': 'Productos electrónicos'},
    {'name': 'Ropa', 'description': 'Prendas de vestir'},
    {'name': 'Alimentos', 'description': 'Productos alimenticios'},
]

for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f"  ✓ Categoría '{cat.name}' creada")

# Productos
products_data = [
    ('Sobre Estándar', 'Documentos', 'Sobre para documentos estándar', 5.00, 0.1),
    ('Caja Pequeña', 'Paquetes', 'Caja pequeña de cartón', 15.00, 0.5),
    ('Caja Mediana', 'Paquetes', 'Caja mediana de cartón', 25.00, 1.0),
    ('Caja Grande', 'Paquetes', 'Caja grande de cartón', 40.00, 2.0),
    ('Laptop', 'Electrónica', 'Laptop de última generación', 800.00, 2.5),
    ('Smartphone', 'Electrónica', 'Smartphone Android', 400.00, 0.3),
    ('T-Shirt', 'Ropa', 'Camiseta de algodón', 20.00, 0.2),
    ('Pantalón', 'Ropa', 'Pantalón denim', 45.00, 0.4),
    ('Kit Gourmet', 'Alimentos', 'Kit de productos gourmet', 65.00, 1.2),
    ('Chocolates Premium', 'Alimentos', 'Caja de chocolates premium', 30.00, 0.5),
]

for name, category_name, description, price, weight in products_data:
    category = Category.objects.get(name=category_name)
    product, created = Product.objects.get_or_create(
        name=name,
        category=category,
        defaults={
            'description': description,
            'price': price,
            'weight': weight
        }
    )
    if created:
        print(f"  ✓ Producto '{product.name}' creado")

# Ciudades - Colombia, México y Estados Unidos
cities_data = [
    # Colombia
    'Bogotá',
    'Medellín',
    'Cali',
    'Barranquilla',
    'Cartagena',
    'Santa Marta',
    # México
    'Ciudad de México',
    'Monterrey',
    'Guadalajara',
    'Cancún',
    # Estados Unidos
    'Miami',
    'Houston',
    'Los Ángeles',
    'Nueva York',
]

for city_name in cities_data:
    city, created = City.objects.get_or_create(name=city_name)
    if created:
        print(f"  ✓ Ciudad '{city.name}' creada")

# Rutas - Red internacional de entrega
routes_data = [
    # Rutas internas Colombia
    ('Bogotá', 'Medellín', 500, 2),
    ('Bogotá', 'Cali', 600, 2),
    ('Medellín', 'Cartagena', 700, 3),
    ('Cali', 'Barranquilla', 900, 3),
    ('Barranquilla', 'Santa Marta', 150, 1),
    ('Medellín', 'Santa Marta', 800, 3),
    ('Cali', 'Cartagena', 400, 2),
    
    # Rutas Colombia - México
    ('Bogotá', 'Ciudad de México', 2100, 5),
    ('Medellín', 'Ciudad de México', 2300, 5),
    ('Cartagena', 'Cancún', 1800, 4),
    
    # Rutas internas México
    ('Ciudad de México', 'Monterrey', 900, 3),
    ('Ciudad de México', 'Guadalajara', 500, 2),
    ('Monterrey', 'Guadalajara', 1200, 3),
    ('Cancún', 'Ciudad de México', 1600, 4),
    
    # Rutas México - Estados Unidos
    ('Monterrey', 'Houston', 800, 2),
    ('Ciudad de México', 'Houston', 1300, 3),
    ('Guadalajara', 'Los Ángeles', 2100, 3),
    ('Cancún', 'Miami', 300, 1),
    
    # Rutas internas Estados Unidos
    ('Houston', 'Miami', 1600, 3),
    ('Houston', 'Nueva York', 2400, 4),
    ('Los Ángeles', 'Miami', 3600, 5),
    ('Los Ángeles', 'Nueva York', 4000, 5),
    ('Miami', 'Nueva York', 1600, 2),
    
    # Rutas directas internacionales
    ('Cartagena', 'Miami', 1200, 2),
    ('Santa Marta', 'Miami', 1400, 2),
    ('Bogotá', 'Miami', 2000, 4),
]

for from_city, to_city, distance, days in routes_data:
    from_obj = City.objects.get(name=from_city)
    to_obj = City.objects.get(name=to_city)
    route, created = Route.objects.get_or_create(
        from_city=from_obj,
        to_city=to_obj,
        defaults={'distance': distance, 'estimated_days': days}
    )
    if created:
        print(f"  ✓ Ruta '{from_city} -> {to_city}' ({distance} km, {days} días) creada")

print("\n" + "=" * 60)
print("✅ CONFIGURACIÓN COMPLETADA")
print("=" * 60)
print("\nPara iniciar el servidor, ejecuta:")
print("  python manage.py runserver")
print("\nLuego accede a:")
print("  http://127.0.0.1:8000/")
print("\n" + "=" * 60)
