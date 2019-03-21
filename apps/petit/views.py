from django.shortcuts import render , redirect
from django.utils.timezone import now
from apps.petit.models import Product, Commerce , Order, Orderdetail
from apps.petit.util import obtenerIP, obtenerFechaExpiracion
from apps.petit.apiTPaga import ApiTPaga
from django.contrib import messages

# Views relacionadas con el comercio


def inicio(request):
        return render(request, 'petit/inicio.html')


def listarProductos(request):
        productos = Product.objects.all()
        return render(
        request, 'petit/productos.html', {"productos": productos})


# Views relacionadas con el pago y el flujo de la solicitud de pago

def hacerOrden(request):
        print("Hola soy Miguelo en python")
        if request.method == 'POST':
                order_id = Order.objects.count() + 1
                n_product = 'Collar GPS'
                v_price = 100
                arr_items = {'name': n_product,
                                'value': v_price}
                total_amount = 100
                k_idcommerce = 1
                terminal_id = Commerce.objects.filter(k_idcommerce=k_idcommerce).values_list('n_commerce', flat=True)
                commerce = [entry for entry in terminal_id]
                #terminal_id = Commerce.objects.filter(k_idcommerce=k_idcommerce).values('n_commerce')
                ip_address = obtenerIP(request)
                expiration_date = obtenerFechaExpiracion()
                print(str(expiration_date))
                requestAPI = ApiTPaga()
                #response = None
                response = requestAPI.solicitar_hacer_pago(
                order_id, ip_address, str(commerce), arr_items, total_amount, str(expiration_date))
                print(response['idempotency_token'])
                print(response['tpaga_payment_url'])
                if "error_code" in response:
                        messages.error(
                                request,
                                'No se pudo completar la transacción'
                        )
                        return redirect('/petit/productos')

                OrderObj, created = Order.objects.create(k_idorder=order_id, f_dateorder=now(
                ), n_tokenorder=response['idempotency_token'], n_status='CRE', v_total=total_amount, k_idcommerce=k_idcommerce)
                if created:
                        OrderObj.save()
                        detail_id = OrderDetail.objects.count() + 1
                        quantity = int(request.POST['cantidad'])
                        OrderDetailObj, createdDetail = OrderDetail.objects.create(
                        k_iddetail=detail_id, q_quantity=quantity, v_subtotal=total_amount, k_idorder=order_id)

                        if createdDetail:
                                OrderDetailObj.save()

                return redirect('/petit/pagar_productos/'+str(order_id))
        else:
                return redirect('/petit/productos')

def pagarOrden(request):
        return render(request,'petit/pagarProductos.html')

def detalleCompra(request):
        return 'hice algo'


def consultaOrden(request):
        return 'lala'


# Views relacionadas con los usuarios
