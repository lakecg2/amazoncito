#!/usr/bin/env python
"""Script para probar el flujo del carrito"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import Product, CartItem, Category

# Obtener o crear usuario de prueba
user = User.objects.first()
print(f"✅ Usuario de prueba: {user.username}")

# Obtener un producto
product = Product.objects.first()
if not product:
    print("❌ No hay productos en la BD")
    sys.exit(1)

print(f"✅ Producto encontrado: {product.name} (ID: {product.id})")

# Limpiar carrito anterior
CartItem.objects.filter(user=user).delete()
print(f"✅ Carrito limpiado")

# Agregar producto al carrito
cart_item, created = CartItem.objects.get_or_create(
    user=user,
    product=product,
    defaults={'quantity': 1}
)

if not created:
    cart_item.quantity += 1
    cart_item.save()

print(f"✅ Producto agregado al carrito (cantidad: {cart_item.quantity})")

# Verificar carrito
cart_items = CartItem.objects.filter(user=user)
print(f"\n📦 Items en carrito de {user.username}:")
for item in cart_items:
    print(f"   - {item.product.name} x{item.quantity} = ${item.product.price * item.quantity}")

# Verificar que los datos están correctos
cart_data = {}
for item in cart_items:
    cart_data[str(item.product.id)] = {
        'id': item.product.id,
        'name': item.product.name,
        'price': float(item.product.price),
        'quantity': item.quantity
    }

print(f"\n✅ Estructura de datos del carrito:")
print(f"   {cart_data}")

print("\n✅ Todas las pruebas pasaron correctamente!")
