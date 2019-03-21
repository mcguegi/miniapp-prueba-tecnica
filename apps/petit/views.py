from django.shortcuts import render



# Views relacionadas con el comercio

def inicio(request):
    return render(request, 'petit/inicio.html')

def listarProductos(request):
    return render(request, 'petit/productos.html')

# Views relacionadas con el pago y el flujo de la solicitud de pago

def productos(request):
    return 'hola'


def detalleCompra(request):
    return 'hice algo'

def consultaOrden(request):
    return 'lala'


# Views relacionadas con los usuarios



