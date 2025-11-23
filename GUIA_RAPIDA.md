# 🚀 GUÍA RÁPIDA DE INICIO

## ⚡ Instalación en 5 minutos

### 1️⃣ Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2️⃣ Instalar Django
```bash
pip install django
```

### 3️⃣ Configurar la base de datos
```bash
python setup_db.py
```

### 4️⃣ Iniciar el servidor
```bash
python manage.py runserver
```

### 5️⃣ Acceder al sitio
🔗 **http://127.0.0.1:8000/**

---

## 🔐 Credenciales de Acceso

### Administrador (Pre-creado)
- **Usuario:** `admin`
- **Contraseña:** `Amazoncito123`

### Cliente (Crear nuevo)
1. Ir a la página de login
2. Clic en pestaña "Registrarse"
3. Llenar formulario
4. ¡Listo!

---

## 📱 Accesos Rápidos

| Rol | URL | Función |
|-----|-----|---------|
| **Público** | http://127.0.0.1:8000/ | Inicio |
| **Cliente** | http://127.0.0.1:8000/client/dashboard/ | Panel principal |
| **Cliente** | http://127.0.0.1:8000/client/orders/ | Mis pedidos |
| **Cliente** | http://127.0.0.1:8000/client/create-order/ | Crear pedido |
| **Admin** | http://127.0.0.1:8000/admin/dashboard/ | Panel admin |
| **Admin** | http://127.0.0.1:8000/admin/services/ | Gestión pedidos |

---

## 📋 Flujo de Prueba

### Como Cliente
1. ✅ Registrarse
2. 📦 Ver productos por categoría
3. 🛒 Crear un pedido (seleccionar productos y ciudad)
4. 📋 Ver mis pedidos
5. 👤 Actualizar perfil
6. ❌ Opcionalmente cancelar un pedido

### Como Administrador
1. 🔐 Iniciar sesión (admin / Amazoncito123)
2. 📊 Ver dashboard con estadísticas
3. 🚚 Ir a servicios
4. ✅ Marcar pedidos como entregados
5. ❌ Cancelar pedidos (notificación al cliente)
6. 👤 Actualizar perfil administrativo

---

## 🎨 Estilos Incluidos

✨ **Diseño Moderno**
- Gradientes atractivos
- Responsive design (móvil + escritorio)
- Animaciones suaves
- Emojis para mejor UX

---

## 🔧 Troubleshooting Rápido

```bash
# Error: ModuleNotFoundError: No module named 'django'
pip install django

# Error: database table doesn't exist
python setup_db.py

# Resetear BD completamente
del db.sqlite3
python setup_db.py

# Ver logs del servidor
# Mirar terminal donde corre manage.py runserver

# Puerto 8000 ocupado
python manage.py runserver 8001
# Acceder a: http://127.0.0.1:8001/
```

---

## 📂 Estructura Mínima Requerida

```
amazoncito/
├── manage.py
├── setup_db.py
├── db.sqlite3 (creado automáticamente)
└── amazoncito/
    ├── settings.py
    ├── urls.py
    ├── views.py
    ├── models.py
    └── templates/
        └── (archivos HTML)
```

---

## 🎯 Objetivos del Proyecto

✅ Sistema de autenticación (login/registro)
✅ Gestión de productos por categorías
✅ Creación y seguimiento de pedidos
✅ Panel de administración
✅ Sistema de notificaciones
✅ Estructuras de datos avanzadas
✅ Base de datos persistente
✅ Interfaz responsive

---

## 📞 Soporte

### Errores comunes y soluciones

**Problema:** "Page not found (404)"
- **Causa:** URL incorrecta
- **Solución:** Verificar la URL en la barra de direcciones

**Problema:** "No module named 'amazoncito'"
- **Causa:** Ubicación incorrecta
- **Solución:** Estar en el directorio del proyecto

**Problema:** "CSRF token missing"
- **Causa:** Formulario sin token
- **Solución:** Ya viene incluido en todos los templates

---

## 🎓 Aprendizaje

Este proyecto implementa:
- 📚 **Backend:** Django (Python)
- 🎨 **Frontend:** HTML, CSS, JavaScript
- 💾 **Base de datos:** SQLite3
- 🏗️ **Estructuras de datos:** LinkedList, Queue, Stack, HashTable, Graph

---

**¡Disfruta usando Amazoncito! 🚚**

Para más detalles, consulta `README.md` y `ESTRUCTURAS_DATOS.md`
