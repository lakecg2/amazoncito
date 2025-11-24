"""
URL configuration for amazoncito project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    
    # Auth URLs
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Client URLs
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('client/account/', views.client_account, name='client_account'),
    path('client/orders/', views.client_orders, name='client_orders'),
    path('client/create-order/', views.create_order, name='create_order'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/account/', views.admin_account, name='admin_account'),
    
    # Cart APIs
    path('api/cart/add/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/get/', views.get_cart, name='get_cart'),
    path('api/cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/clear/', views.clear_cart, name='clear_cart'),
    path('api/cart/update/', views.update_cart_quantity, name='update_cart_quantity'),
    
    # Utility URLs
    path('api/init-admin/', views.initialize_admin, name='init_admin'),
    path('api/init-data/', views.initialize_data, name='init_data'),
]
