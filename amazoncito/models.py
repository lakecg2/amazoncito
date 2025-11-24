from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Estructuras de datos

class Node:
    """Nodo para listas enlazadas"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Lista enlazada simple"""
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def to_list(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

class Queue:
    "Cola"
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

class Stack:
    """Pila"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

class HashTable:
    """Tabla hash con polinomio de direccionamiento"""
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def hash_polynomial(self, key):
        """Función hash con polinomio de direccionamiento"""
        hash_value = 0
        p = 31
        p_pow = 1
        for char in str(key):
            hash_value = (hash_value + (ord(char) * p_pow)) % (10**9 + 9)
            p_pow = (p_pow * p) % (10**9 + 9)
        return hash_value % self.size
    
    def insert(self, key, value):
        index = self.hash_polynomial(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
    
    def search(self, key):
        index = self.hash_polynomial(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        index = self.hash_polynomial(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index].pop(i)
                return True
        return False

class Graph:
    """Grafo para rutas de entrega"""
    def __init__(self):
        self.vertices = {}
        self.edges = {}
    
    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = True
            self.edges[vertex] = []
    
    def add_edge(self, v1, v2, weight=1):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.edges[v1].append((v2, weight))
        self.edges[v2].append((v1, weight))
    
    def bfs_shortest_path(self, start, end):
        """BFS para encontrar la ruta más corta"""
        if start not in self.vertices or end not in self.vertices:
            return None
        
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            
            for neighbor, _ in self.edges.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None

# Modelos Django

class UserProfile(models.Model):
    """Perfil extendido del usuario"""
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cliente')
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Category(models.Model):
    """Categoría de productos"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Producto de la paquetería"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    """Pedido de entrega"""
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    destination_city = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=50, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancellation_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.tracking_number} - {self.user.username}"

class OrderItem(models.Model):
    """Items en un pedido"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class City(models.Model):
    """Ciudad para rutas de entrega"""
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Route(models.Model):
    """Ruta entre ciudades"""
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_routes')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_routes')
    distance = models.IntegerField()
    estimated_days = models.IntegerField()
    
    def __str__(self):
        return f"{self.from_city} -> {self.to_city}"

class DeliveryHistory(models.Model):
    """Historial de entregas completadas (Pila)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Delivery of {self.order.tracking_number}"

class NotificationMessage(models.Model):
    """Mensajes de notificación para usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username}"

class CartItem(models.Model):
    """Items en el carrito del cliente"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'product')
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} x{self.quantity}"

class DeliveryEstimate(models.Model):
    """Estimación de entrega para órdenes"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_estimate')
    estimated_arrival = models.DateTimeField()
    route_path = models.TextField()  # JSON con la ruta: [ciudad1, ciudad2, ...]
    total_distance = models.IntegerField(default=0)  # Distancia total en km
    
    def __str__(self):
        return f"Delivery estimate for {self.order.tracking_number}"