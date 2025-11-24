#!/usr/bin/env python
"""Script para probar la renderización del template create_order"""

import os
import sys
import django
from django.template import Template, Context
from django.template.loader import get_template

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import Product, CartItem, Category

# Obtener usuario y limpiar su carrito
user = User.objects.first()
CartItem.objects.filter(user=user).delete()

# Agregar algunos productos al carrito
products = Product.objects.all()[:3]
for idx, product in enumerate(products, start=1):
    CartItem.objects.create(user=user, product=product, quantity=idx)

print(f"✅ Usuario: {user.username}")
print(f"✅ Productos en carrito: {CartItem.objects.filter(user=user).count()}")

# Obtener los datos que se pasarían al template
categories = Category.objects.all()
products_by_category = {}
for category in categories:
    products_by_category[category.name] = list(category.products.all())

cart_items = CartItem.objects.filter(user=user).select_related('product')
cart_data = {}
for item in cart_items:
    cart_data[str(item.product.id)] = {
        'id': item.product.id,
        'name': item.product.name,
        'price': float(item.product.price),
        'quantity': item.quantity
    }

context = {
    'cities': [],
    'categories': categories,
    'products_by_category': products_by_category,
    'cart': cart_data,
}

# Intentar renderizar el template
try:
    template = get_template('client/create_order.html')
    html = template.render(context)
    
    # Verificar que el carrito se renderizó correctamente
    if 'cart = {' in html:
        print("✅ Variable 'cart' renderizada correctamente en JavaScript")
    else:
        print("❌ Variable 'cart' NO se encontró en el HTML")
        
    # Verificar que el carrito tiene los datos correctos
    for product_id, item_data in cart_data.items():
        if str(product_id) in html:
            print(f"✅ Producto ID {product_id} encontrado en HTML")
        else:
            print(f"❌ Producto ID {product_id} NO encontrado en HTML")
    
    # Guardar el HTML para inspección
    with open('test_create_order.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ HTML guardado en test_create_order.html")
    
    # Buscar líneas clave en el HTML
    lines = html.split('\n')
    for i, line in enumerate(lines):
        if 'let cart = {' in line:
            print(f"\n📍 Línea {i+1}: {line[:80]}")
            # Mostrar las siguientes 10 líneas
            for j in range(i+1, min(i+11, len(lines))):
                print(f"   {lines[j][:80]}")
            break
    
    print("\n✅ Renderización completada exitosamente")
    
except Exception as e:
    print(f"❌ Error al renderizar template: {e}")
    import traceback
    traceback.print_exc()
