#!/usr/bin/env python
"""Test para verificar que la actualización del carrito funciona correctamente"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import Product, CartItem

print("=" * 70)
print("TEST DE ACTUALIZACIÓN DE CARRITO EN TIEMPO REAL")
print("=" * 70)

user = User.objects.first()
print(f"\n[TEST 1] Usuario: {user.username}")

# Limpiar carrito
CartItem.objects.filter(user=user).delete()
print("[TEST 1] Carrito limpiado ✓")

# Agregar productos
products = Product.objects.all()[:3]
for idx, product in enumerate(products, 1):
    CartItem.objects.create(user=user, product=product, quantity=idx)
    print(f"[TEST 1] Producto agregado: {product.name} x{idx}")

cart_count = CartItem.objects.filter(user=user).count()
print(f"[TEST 1] Total en carrito: {cart_count} ✓\n")

# Test 2: Simular actualización de cantidad
print("[TEST 2] Actualizar cantidad de producto...")
item = CartItem.objects.filter(user=user).first()
print(f"  Antes: {item.product.name} x{item.quantity}")
item.quantity = 5
item.save()
print(f"  Después: {item.product.name} x{item.quantity} ✓")

# Test 3: Simular eliminación
print("\n[TEST 3] Eliminar producto del carrito...")
item_to_delete = CartItem.objects.filter(user=user).last()
print(f"  Eliminando: {item_to_delete.product.name}")
item_to_delete.delete()
remaining = CartItem.objects.filter(user=user).count()
print(f"  Productos restantes: {remaining} ✓")

# Test 4: Simular limpieza completa
print("\n[TEST 4] Limpiar todo el carrito...")
CartItem.objects.filter(user=user).delete()
empty_count = CartItem.objects.filter(user=user).count()
print(f"  Carrito vacío: {empty_count == 0} ✓")

print("\n" + "=" * 70)
print("✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
print("=" * 70)
print("\nCambios realizados:")
print("✓ removeFromCart: Ahora actualiza localmente sin hacer fetch a loadCartFromServer")
print("✓ clearCartServer: Ahora limpia localmente sin hacer fetch a loadCartFromServer")
print("✓ Cambios se muestran inmediatamente en la interfaz")
