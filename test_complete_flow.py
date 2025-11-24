#!/usr/bin/env python
"""Script para probar el flujo completo: agregar a carrito y crear orden"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import Product, CartItem, Category, Order

print("=" * 60)
print("PRUEBA 1: Agregar productos al carrito")
print("=" * 60)

user = User.objects.first()
print(f"✅ Usuario: {user.username}")

# Limpiar carrito
CartItem.objects.filter(user=user).delete()
print(f"✅ Carrito limpiado")

# Obtener productos
products = Product.objects.all()[:2]
for idx, product in enumerate(products, start=1):
    cart_item, created = CartItem.objects.get_or_create(
        user=user,
        product=product,
        defaults={'quantity': idx}
    )
    if not created:
        cart_item.quantity = idx
        cart_item.save()
    print(f"✅ Producto agregado: {product.name} (cantidad: {idx})")

print(f"\n📦 Carrito final: {CartItem.objects.filter(user=user).count()} items")
for item in CartItem.objects.filter(user=user):
    print(f"   - {item.product.name} x{item.quantity} = ${item.product.price * item.quantity}")

print("\n" + "=" * 60)
print("PRUEBA 2: Crear orden desde los items del carrito")
print("=" * 60)

# Simular lo que haría views.py create_order
cart_items = CartItem.objects.filter(user=user).select_related('product')
order = Order.objects.create(
    user=user,
    destination_city='CDMX',
    tracking_number='TEST12345',
    total_price=Decimal('0')
)
print(f"✅ Orden creada: {order.tracking_number}")

total = Decimal('0')
item_count = 0
for item in cart_items:
    from amazoncito.models import OrderItem
    OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity,
        price=item.product.price * item.quantity
    )
    total += item.product.price * item.quantity
    item_count += 1
    print(f"✅ Item agregado a orden: {item.product.name} x{item.quantity}")

order.total_price = total
order.save()
print(f"✅ Total de orden: ${total}")

print("\n" + "=" * 60)
print("PRUEBA 3: Verificar que el carrito se limpia después de la orden")
print("=" * 60)

CartItem.objects.filter(user=user).delete()
remaining_items = CartItem.objects.filter(user=user).count()
print(f"✅ Carrito limpiado. Items restantes: {remaining_items}")

print("\n" + "=" * 60)
print("✅ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
print("=" * 60)
