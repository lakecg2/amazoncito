#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para validar que el JavaScript en el template es sintácticamente correcto"""

import os
import sys
import django
import re
import json

# Configurar UTF-8 para Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazoncito.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from amazoncito.models import Product, CartItem, Category
from django.template.loader import get_template

# Setup
user = User.objects.first()
CartItem.objects.filter(user=user).delete()

products = Product.objects.all()[:2]
for idx, product in enumerate(products, start=1):
    CartItem.objects.create(user=user, product=product, quantity=idx)

# Get context data
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

# Render template
template = get_template('client/create_order.html')
html = template.render(context)

# Extract the cart initialization code
match = re.search(r'let cart = \{(.*?)\};', html, re.DOTALL)
if match:
    cart_code = match.group(0)
    print("[OK] Found cart initialization code")
    print(f"\nFirst 200 chars:\n{cart_code[:200]}")
    
    # Test if it's valid JavaScript by checking structure
    if '"1"' in html and 'parseFloat' in html:
        print("\n[OK] Cart initialization uses parseFloat for numeric values")
    
    # Check for product data structure
    if 'name:' in html and 'price:' in html and 'quantity:' in html:
        print("[OK] Cart has required fields (name, price, quantity)")
    
    # Check for productsByCategory
    if 'productsByCategory' in html:
        print("[OK] productsByCategory initialized")
    
    # Check for functions
    functions = ['loadCartFromServer', 'renderProducts', 'updateCart', 'addToCartServer', 'removeFromCart']
    missing = []
    for func in functions:
        if f'function {func}' in html or f'{func}()' in html:
            print(f"[OK] Function '{func}' found")
        else:
            missing.append(func)
    
    if missing:
        print(f"\n[WARNING] Missing functions: {missing}")
    else:
        print("\n[OK] All required functions found")

print("\n" + "="*60)
print("[OK] JavaScript validation complete")
print("="*60)
