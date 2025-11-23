from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum
from decimal import Decimal
import uuid
import json

from .models import (
    UserProfile, Product, Category, Order, OrderItem, 
    DeliveryHistory, NotificationMessage, City, Route, Graph
)

# Vistas de autenticación

def login_view(request):
    """Vista de login/registro"""
    if request.user.is_authenticated:
        return redirect_by_role(request)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if action == 'login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_by_role(request)
            else:
                return render(request, 'auth/login.html', {'error': 'Credenciales inválidas'})
        
        elif action == 'register':
            password2 = request.POST.get('password2')
            email = request.POST.get('email', '')
            
            if password != password2:
                return render(request, 'auth/login.html', {'error': 'Las contraseñas no coinciden'})
            
            if User.objects.filter(username=username).exists():
                return render(request, 'auth/login.html', {'error': 'El usuario ya existe'})
            
            user = User.objects.create_user(username=username, password=password, email=email)
            profile = UserProfile.objects.create(user=user, role='cliente')
            login(request, user)
            return redirect('client_dashboard')
    
    return render(request, 'auth/login.html')

def redirect_by_role(request):
    """Redirige según el rol del usuario"""
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    
    try:
        profile = UserProfile.objects.get(user=user)
        if profile.role == 'admin':
            return redirect('admin_dashboard')
        else:
            return redirect('client_dashboard')
    except UserProfile.DoesNotExist:
        # Si no existe perfil, crear uno como cliente
        UserProfile.objects.create(user=user, role='cliente')
        return redirect('client_dashboard')

@login_required(login_url='login')
def logout_view(request):
    """Vista de logout"""
    logout(request)
    return redirect('login')

# Vistas para clientes

@login_required(login_url='login')
def client_dashboard(request):
    """Dashboard principal del cliente"""
    # Verificar rol
    try:
        profile = request.user.userprofile
        if profile.role != 'cliente':
            return redirect('admin_dashboard')
    except:
        return redirect('login')
    
    # Obtener categorías y productos usando estructuras de datos
    categories = Category.objects.all()
    products_by_category = {}
    
    for category in categories:
        products_by_category[category.name] = list(category.products.all())
    
    # Obtener notificaciones no leídas
    notifications = NotificationMessage.objects.filter(user=request.user, is_read=False)
    
    context = {
        'categories': categories,
        'products_by_category': products_by_category,
        'notifications': notifications,
    }
    return render(request, 'client/dashboard.html', context)

@login_required(login_url='login')
def client_account(request):
    """Gestión de cuenta del cliente"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        description = request.POST.get('description', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        
        profile.description = description
        profile.address = address
        profile.phone = phone
        profile.save()
        
        return render(request, 'client/account.html', {
            'profile': profile,
            'success': 'Perfil actualizado correctamente'
        })
    
    return render(request, 'client/account.html', {'profile': profile})

@login_required(login_url='login')
def client_orders(request):
    """Ver pedidos del cliente"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        
        if action == 'cancel':
            order = get_object_or_404(Order, id=order_id, user=request.user)
            cancellation_message = request.POST.get('cancellation_message', 'Cancelado por el cliente')
            
            if order.status not in ['entregado', 'cancelado']:
                order.status = 'cancelado'
                order.cancellation_message = cancellation_message
                order.save()
    
    # Cargar notificaciones
    for order in orders:
        notifications = NotificationMessage.objects.filter(order=order, user=request.user, is_read=False)
        for notif in notifications:
            notif.is_read = True
            notif.save()
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {'orders': orders}
    return render(request, 'client/orders.html', context)

@login_required(login_url='login')
def create_order(request):
    """Crear un nuevo pedido"""
    if request.method == 'POST':
        destination_city = request.POST.get('destination_city')
        items = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        
        if not items or not destination_city:
            return JsonResponse({'error': 'Faltan datos'}, status=400)
        
        # Crear orden
        tracking_number = str(uuid.uuid4())[:12].upper()
        order = Order.objects.create(
            user=request.user,
            destination_city=destination_city,
            tracking_number=tracking_number,
            total_price=0
        )
        
        total_price = Decimal('0')
        
        # Agregar items usando estructura de cola
        order_queue = []
        for product_id, quantity in zip(items, quantities):
            try:
                product = Product.objects.get(id=product_id)
                qty = int(quantity)
                price = product.price * qty
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=price
                )
                
                order_queue.append({
                    'product': product.name,
                    'quantity': qty,
                    'price': float(price)
                })
                
                total_price += price
            except Product.DoesNotExist:
                pass
        
        order.total_price = total_price
        order.save()
        
        return JsonResponse({
            'success': True,
            'tracking_number': tracking_number,
            'order_id': order.id
        })
    
    cities = City.objects.all()
    categories = Category.objects.all()
    products_by_category = {}
    
    for category in categories:
        products_by_category[category.name] = list(category.products.all())
    
    context = {
        'cities': cities,
        'categories': categories,
        'products_by_category': products_by_category,
    }
    return render(request, 'client/create_order.html', context)

# Vistas para administrador

@login_required(login_url='login')
def admin_dashboard(request):
    """Dashboard del administrador"""
    try:
        profile = request.user.userprofile
        if profile.role != 'admin':
            return redirect('client_dashboard')
    except:
        return redirect('login')
    
    # Estadísticas usando estructuras de datos
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pendiente').count()
    delivered_orders = Order.objects.filter(status='entregado').count()
    total_revenue = Order.objects.filter(status='entregado').aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='login')
def admin_services(request):
    """Gestión de servicios y pedidos para administrador"""
    try:
        profile = request.user.userprofile
        if profile.role != 'admin':
            return redirect('client_dashboard')
    except:
        return redirect('login')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        
        if action == 'delete':
            order = get_object_or_404(Order, id=order_id)
            cancellation_message = request.POST.get('cancellation_message', 'Cancelado por administración')
            
            # Crear notificación para el cliente
            NotificationMessage.objects.create(
                user=order.user,
                order=order,
                message=f"Tu pedido {order.tracking_number} ha sido cancelado. Motivo: {cancellation_message}"
            )
            
            order.status = 'cancelado'
            order.cancellation_message = cancellation_message
            order.save()
        
        elif action == 'complete':
            order = get_object_or_404(Order, id=order_id)
            order.status = 'entregado'
            order.save()
            
            # Agregar al historial de entregas (pila)
            DeliveryHistory.objects.create(order=order, notes="Entregado exitosamente")
            
            # Crear notificación para el cliente
            NotificationMessage.objects.create(
                user=order.user,
                order=order,
                message=f"Tu pedido {order.tracking_number} ha sido entregado exitosamente"
            )
    
    # Usar cola para procesar pedidos pendientes
    pending_orders_queue = Order.objects.filter(status='pendiente').order_by('created_at')
    all_orders = Order.objects.all().order_by('-created_at')
    
    context = {
        'pending_orders': pending_orders_queue,
        'all_orders': all_orders,
    }
    return render(request, 'admin/services.html', context)

@login_required(login_url='login')
def admin_account(request):
    """Gestión de cuenta del administrador"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        description = request.POST.get('description', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        
        profile.description = description
        profile.address = address
        profile.phone = phone
        profile.save()
        
        return render(request, 'admin/account.html', {
            'profile': profile,
            'success': 'Perfil actualizado correctamente'
        })
    
    return render(request, 'admin/account.html', {'profile': profile})

# Vistas de utilidad

def initialize_admin(request):
    """Inicializar usuario administrador (solo si no existe)"""
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(username='admin', password='Amazoncito123')
        UserProfile.objects.create(user=admin_user, role='admin')
        return JsonResponse({'message': 'Admin user created'})
    return JsonResponse({'message': 'Admin user already exists'})

def initialize_data(request):
    """Inicializar datos de prueba"""
    # Crear categorías
    categories_data = ['Documentos', 'Paquetes', 'Electrónica', 'Ropa', 'Alimentos']
    for cat_name in categories_data:
        Category.objects.get_or_create(name=cat_name)
    
    # Crear productos
    products_data = [
        ('Sobre Estándar', 'Documentos', 5.00, 0.1),
        ('Caja Pequeña', 'Paquetes', 15.00, 0.5),
        ('Caja Mediana', 'Paquetes', 25.00, 1.0),
        ('Caja Grande', 'Paquetes', 40.00, 2.0),
        ('Laptop', 'Electrónica', 800.00, 2.5),
        ('Smartphone', 'Electrónica', 400.00, 0.3),
        ('T-Shirt', 'Ropa', 20.00, 0.2),
        ('Pantalón', 'Ropa', 45.00, 0.4),
        ('Kit Gourmet', 'Alimentos', 65.00, 1.2),
        ('Chocolates Premium', 'Alimentos', 30.00, 0.5),
    ]
    
    for name, category_name, price, weight in products_data:
        category = Category.objects.get(name=category_name)
        Product.objects.get_or_create(
            name=name,
            category=category,
            defaults={
                'description': f'Producto {name}',
                'price': price,
                'weight': weight
            }
        )
    
    # Crear ciudades
    cities_data = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Santa Marta']
    for city_name in cities_data:
        City.objects.get_or_create(name=city_name)
    
    # Crear rutas
    routes_data = [
        ('Bogotá', 'Medellín', 500, 2),
        ('Bogotá', 'Cali', 600, 2),
        ('Medellín', 'Cartagena', 700, 3),
        ('Cali', 'Barranquilla', 900, 3),
        ('Barranquilla', 'Santa Marta', 150, 1),
    ]
    
    for from_city, to_city, distance, days in routes_data:
        from_obj = City.objects.get(name=from_city)
        to_obj = City.objects.get(name=to_city)
        Route.objects.get_or_create(
            from_city=from_obj,
            to_city=to_obj,
            defaults={'distance': distance, 'estimated_days': days}
        )
    
    return JsonResponse({'message': 'Data initialized'})