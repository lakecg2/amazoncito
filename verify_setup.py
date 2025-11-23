#!/usr/bin/env python
"""
Script para verificar que la base de datos está correctamente configurada.
Ejecutar: python verify_setup.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import UserProfile, Category, Product, City, Route

print("=" * 60)
print("VERIFICACIÓN DE CONFIGURACIÓN - Amazoncito")
print("=" * 60)

# Verificar usuarios
print("\n👤 USUARIOS Y ROLES:")
print("-" * 60)
users = User.objects.all()
for user in users:
    try:
        profile = UserProfile.objects.get(user=user)
        print(f"  ✓ {user.username:20} | Rol: {profile.role:10} | Email: {user.email}")
    except:
        print(f"  ⚠️ {user.username:20} | ¡SIN PERFIL!")

# Verificar admin específicamente
print("\n🔐 USUARIO ADMINISTRADOR:")
print("-" * 60)
admin = User.objects.filter(username='admin').first()
if admin:
    profile = UserProfile.objects.filter(user=admin).first()
    if profile and profile.role == 'admin':
        print(f"  ✓ Admin configurado correctamente")
        print(f"    Usuario: admin")
        print(f"    Contraseña: Amazoncito123")
        print(f"    Rol: {profile.role}")
    else:
        print(f"  ⚠️ Admin existe pero rol es incorrecto: {profile.role if profile else 'SIN PERFIL'}")
else:
    print(f"  ⚠️ Usuario admin no existe")

# Verificar categorías
print("\n📦 CATEGORÍAS:")
print("-" * 60)
categories = Category.objects.all()
print(f"  Total: {categories.count()}")
for cat in categories:
    print(f"  ✓ {cat.name}")

# Verificar productos
print("\n🛍️  PRODUCTOS:")
print("-" * 60)
products = Product.objects.all()
print(f"  Total: {products.count()}")
for prod in products[:3]:
    print(f"  ✓ {prod.name:20} | {prod.category.name:15} | ${prod.price}")
if products.count() > 3:
    print(f"  ... y {products.count() - 3} más")

# Verificar ciudades
print("\n🌍 CIUDADES:")
print("-" * 60)
cities = City.objects.all()
print(f"  Total: {cities.count()}")
for city in cities:
    print(f"  ✓ {city.name}")

# Verificar rutas
print("\n🚚 RUTAS:")
print("-" * 60)
routes = Route.objects.all()
print(f"  Total: {routes.count()}")
for route in routes[:3]:
    print(f"  ✓ {route.from_city.name:15} -> {route.to_city.name:15} | {route.distance}km")
if routes.count() > 3:
    print(f"  ... y {routes.count() - 3} más")

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 60)
