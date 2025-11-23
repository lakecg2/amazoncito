# 🚚 Amazoncito - Sistema de Gestión de Paqueterías

## Descripción del Proyecto

Sistema completo de gestión de paqueterías desarrollado en **Django** e **HTML/CSS/JavaScript**. Implementa estructuras de datos avanzadas (listas enlazadas, colas, pilas, tablas hash y grafos) para optimizar la gestión de clientes, pedidos y rutas de entrega.

### Características Principales

#### Para Clientes
- ✅ Registro e inicio de sesión
- 📦 Visualización de productos por categorías
- 🛒 Creación de pedidos con múltiples productos
- 📋 Historial de pedidos con estado en tiempo real
- 💬 Notificaciones de cancelación de pedidos
- 👤 Gestión de perfil personal
- 🚪 Cierre de sesión seguro

#### Para Administradores
- 📊 Dashboard con estadísticas en tiempo real
- 🚚 Panel de gestión de servicios
- 📋 Visualización de todos los pedidos
- ✅ Marcar pedidos como entregados
- ❌ Cancelar pedidos con mensaje de notificación
- 📬 Sistema de notificaciones para clientes
- 👤 Gestión de cuenta administrativa

### Estructuras de Datos Implementadas

1. **Listas Enlazadas** - Gestión de productos y categorías
2. **Colas (FIFO)** - Procesamiento de pedidos pendientes
3. **Pilas (LIFO)** - Historial de entregas completadas
4. **Tablas Hash** - Búsqueda eficiente de clientes (función polinómica)
5. **Grafos** - Modelado de rutas de entrega entre ciudades (BFS para ruta más corta)

## Requisitos

- Python 3.8+
- Django 5.2+
- SQLite3 (incluido en Django)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd amazoncito
```

### 2. Crear e activar entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django
```

### 4. Configurar la base de datos

```bash
python setup_db.py
```

Este script realizará:
- Creación de migraciones
- Aplicación de migraciones
- Creación de usuario administrador (admin / Amazoncito123)
- Carga de datos iniciales (categorías, productos, ciudades, rutas)

## Uso

### Iniciar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

### Acceder al Sistema

**Inicio de la aplicación:**
- URL: `http://127.0.0.1:8000/`

**Credenciales de Administrador:**
- Usuario: `admin`
- Contraseña: `Amazoncito123`

### Crear Nuevo Cliente

1. En la página de login, hacer clic en la pestaña "Registrarse"
2. Completar el formulario con:
   - Usuario
   - Email (opcional)
   - Contraseña
   - Confirmación de contraseña
3. Presionar "Registrarse"

## Estructura del Proyecto

```
amazoncito/
├── manage.py                 # Utilidad de Django
├── setup_db.py              # Script de inicialización
├── db.sqlite3               # Base de datos SQLite
├── amazoncito/
│   ├── __init__.py
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # Enrutamiento de URLs
│   ├── views.py             # Lógica de vistas
│   ├── models.py            # Modelos y estructuras de datos
│   ├── wsgi.py
│   ├── asgi.py
│   └── templates/
│       ├── auth/
│       │   └── login.html               # Página de autenticación
│       ├── core/
│       │   └── index.html               # Página de inicio
│       ├── client/
│       │   ├── dashboard.html           # Dashboard cliente
│       │   ├── create_order.html        # Crear pedidos
│       │   ├── orders.html              # Mis pedidos
│       │   └── account.html             # Mi cuenta
│       └── admin/
│           ├── dashboard.html           # Dashboard admin
│           ├── services.html            # Gestión de servicios
│           └── account.html             # Cuenta admin
└── README.md                # Este archivo
```

## Rutas de la Aplicación

### Públicas
- `/` - Página de inicio
- `/` - Login/Registro

### Clientes (requieren autenticación)
- `/client/dashboard/` - Panel principal del cliente
- `/client/orders/` - Mis pedidos
- `/client/create-order/` - Crear nuevo pedido
- `/client/account/` - Gestión de perfil
- `/logout/` - Cerrar sesión

### Administrador (requiere autenticación como admin)
- `/admin/dashboard/` - Panel de control
- `/admin/services/` - Gestión de servicios
- `/admin/account/` - Cuenta del administrador
- `/logout/` - Cerrar sesión

### API (inicialización)
- `/api/init-admin/` - Crear usuario administrador
- `/api/init-data/` - Cargar datos iniciales

## Funcionalidades Avanzadas

### Sistema de Notificaciones
- Cuando un administrador cancela un pedido, se genera una notificación
- Los clientes ven las notificaciones la próxima vez que inician sesión
- Se marca como leída automáticamente al abrir los pedidos

### Gestión de Pedidos
- **Estado**: Pendiente → Procesando → Enviado → Entregado (o Cancelado)
- **Número de seguimiento**: Identificador único para cada pedido
- **Historial de entregas**: Se almacena en una pila (LIFO)

### Búsqueda de Clientes
Utiliza tabla hash con función polinómica de direccionamiento para búsquedas $O(1)$

### Rutas de Entrega
- Modeladas como grafo conectado
- Implementación de BFS para encontrar ruta más corta
- Cálculo de distancia entre ciudades

## Estilos

Todos los estilos están implementados **inline en los archivos HTML** sin utilizar archivos CSS externos. Esto incluye:

- Colores: Gradientes modernos (púrpura/azul y rojo/naranja)
- Responsive Design: Adaptable a móviles y escritorio
- Iconos: Emojis para mejor UX
- Animaciones: Transiciones suaves en botones y tarjetas

## Base de Datos - Modelos

### UserProfile
- Extiende el usuario de Django
- Rol: Cliente o Administrador
- Descripción personal
- Dirección y teléfono

### Product
- Nombre, descripción
- Precio y peso
- Categoría asociada

### Category
- Nombre único
- Descripción

### Order
- Usuario asociado
- Estado (pendiente, procesando, enviado, entregado, cancelado)
- Ciudad de destino
- Número de seguimiento
- Mensaje de cancelación

### OrderItem
- Producto específico
- Cantidad y precio

### City
- Nombre de la ciudad
- Código postal

### Route
- Ciudades origen y destino
- Distancia y días estimados

### DeliveryHistory
- Pila de entregas completadas
- Fecha de entrega
- Notas adicionales

### NotificationMessage
- Mensajes para usuarios
- Referencia a pedido
- Estado de lectura

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder a la consola interactiva
python manage.py shell

# Ver estructura de BD
python manage.py sqlmigrate amazoncito 0001

# Crear tabla personalizada
python manage.py migrate

# Resetear la BD (borrar y recrear)
rm db.sqlite3
python setup_db.py
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'django'"
**Solución:** Instalar Django con `pip install django`

### Error: "No such table"
**Solución:** Ejecutar `python setup_db.py` para crear la BD

### Error: "Reverse for 'url_name' not found"
**Solución:** Verificar que el nombre de la URL en `urls.py` coincida con el template

### Error 404 en templates
**Solución:** Verificar que TEMPLATES['DIRS'] en settings.py apunte a la carpeta correcta

## Notas de Desarrollo

- El sistema utiliza sesiones de Django para autenticación
- Todos los datos se validan en servidor (backend)
- Las transacciones de pedidos son atómicas
- Los permisos se verifican con decoradores `@login_required`

## Autor

Desarrollo para proyecto de Estructuras de Datos y sus Aplicaciones

## Licencia

Este proyecto es de carácter educativo.

---

**¡Gracias por usar Amazoncito! 🚚**
