from django.contrib import admin
from django.urls import path , include
from apps.petit import views

app_name = 'petit'

urlpatterns = [
    path('inicio', views.inicio),
    path('productos', views.listarProductos),
    path('detalleCompra', views.detalleCompra),
    path('consultarOrden' , views.consultaOrden),


]
