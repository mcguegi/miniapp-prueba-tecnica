from django.contrib import admin
from django.urls import path , include
from apps.petit import views

app_name = 'petit'

urlpatterns = [
    path('inicio', views.inicio , name='inicio'),
    path('productos', views.listarProductos, name='listarProductos'),
    path('hacerOrden', views.hacerOrden, name='hacerOrden'),
    path('pagarOrden', views.pagarOrden, name='pagarOrden'),
    path('detalleCompra', views.detalleCompra , name= 'detalleCompra'),
    path('consultarOrden' , views.consultaOrden, name= 'consultarOrden'),


]
