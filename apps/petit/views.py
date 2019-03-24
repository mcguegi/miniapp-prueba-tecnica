from django.shortcuts import render, redirect
from django.utils.timezone import now
from apps.petit.models import Product, Customer, Orderbill, Orderbilldetail
from apps.petit.util import obtenerIP, obtenerFechaExpiracion
from apps.petit.apiTPaga import ApiTPaga
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
import logging

# Views relacionadas con el comercio y sus productos

def inicio(request):
 return render(request, 'petit/inicio.html')

def listarProductos(request):
  productos = Product.objects.all()
  return render(
  request, 'petit/productos.html', {"productos": productos})


# Views relacionadas con el pago y el flujo de la solicitud de pago

def hacerOrden(request):
 if request.method == 'POST':
  requestObj = request.POST
  if(data is None):
    return HttpResponseBadRequest()
  else :
    order_id = Orderbill.objects.count() + 1
    n_product = str(requestObj.get('product_name1', False))
    v_price = int(requestObj.get('product_price1', False))
    q_quantity = str(requestObj.get('quantity', False))
    q = int(q_quantity)
    price = int(v_price)
    product = Product.objects.get(n_product=n_product)
    customer = Customer.objects.get(k_id='1032488586')
    customerId = customer.k_id

    arr_items = []
    for purchase_item in range(1, q+1):
     item = {'name': n_product,
     'value': price}
     arr_items.append(item)
     
    total_amount = q*price
    terminal_id = 'Petit'
    ip_address = obtenerIP(request)
    expiration_date = obtenerFechaExpiracion()

    requestAPI = ApiTPaga()
    responseOrder = None

    responseOrder = requestAPI.solicitar_hacer_pago(
    order_id, ip_address, terminal_id, arr_items, total_amount, str(expiration_date))

    print(responseOrder)

    if "error_code" in responseOrder:
      messages.error(
       request,
       'No se pudo completar la transacción'
       )
      return redirect('/petit/productos')

    OrderObj, created = Orderbill.objects.get_or_create(k_idorderbill=order_id, f_dateorderbill=now(
        ), n_tokenorderbill=responseOrder['token'], n_tokenpayment = responseOrder['tpaga_payment_url'], n_status='CRE', v_total=total_amount, k=customer)

    if created:
      OrderObj.save()
      detail_id = Orderbilldetail.objects.count() + 1
      OrderDetailObj, createdDetail = Orderbilldetail.objects.get_or_create(
        k_iddetail=detail_id, q_quantity=q, v_subtotal=total_amount, k_idorderbill=OrderObj, k_idproduct=product)

      if createdDetail:
        OrderDetailObj.save()
        return redirect('/petit/pagarOrden/' + str(order_id))
      else:
        return redirect('/petit/productos')

def pagarOrden(request , order_id):
  try:
    order = Orderbill.objects.get(k_idorderbill = order_id)
  except Order.DoesNotExist:
    raise Http404

  details = Orderbilldetail.objects.filter(k_idorderbill = order_id)
  arr_items = []

  for detail in details:
    kproducto = detail.k_idproduct
    p = str(kproducto)
    q = detail.q_quantity
    print(str(kproducto))
    print(type(p))
    product = Product.objects.get(k_idproduct = int(p))
    productDict = {
                "name" : product.n_product,
                "value" : product.v_price
              }
  arr_items.append(productDict)

  contextPayOrder = {"order" : order ,
                    "products" : productDict,
                    "quantity" : q
                    }

  return render(request,'petit/pagarProductos.html' , contextPayOrder)

def confirmarPago(request , order_id):
  try:
    order = Orderbill.objects.get(k_idorderbill = order_id)
    token = str(order.n_tokenorderbill)
    requestAPI = ApiTPaga()
    responsePay = None
    responsePay = requestAPI.confirmar_estado_sol_pago(token)
    if "error_code" in responsePay:
      logger.error('{} {}'.format(responsePay.status_code, responsePay.json()))

    print(responsePay)
    status_order = responsePay['status']

    if order.n_status == "CRE":
      statusResponse = responsePay["status"]
      orderU = Orderbill.objects.filter(k_idorderbill = order_id).update(n_status= statusResponse[:3].upper())

    details = Orderbilldetail.objects.filter(k_idorderbill = order_id)
    arr_items = []

    for detail in details:
      kproducto = detail.k_idproduct
      q = detail.q_quantity
      p = str(kproducto)
      product = Product.objects.get(k_idproduct = int(p))
      productDict = {
                  "name" : product.n_product,
                  "value" : product.v_price
                }
      arr_items.append(productDict)

    contextCheckPay = {"order" : order , "products" : productDict , "quantity" : q}
    return render(request, 'petit/confirmarPago.html', contextCheckPay)

  except Orderbill.DoesNotExist:
    raise Http404
    return redirect('petit/pagarProductos' + str(order_id))

@login_required(login_url='/login/')
def consultarTransacciones(request):
  orders = Orderbilldetail.objects.select_related('k_idorderbill').select_related('k_idproduct').all().order_by('k_idorderbill')
  contextTransactions = {"orders" : orders}
  return render(request,'petit/consultarTransacciones.html',contextTransactions)

@login_required(login_url='/login/')
def revertirPago(request):
  if request.method == 'POST':
    requestObj = request.POST
    order_id = int(requestObj.get('order_id',False))
    try:
      order = Orderbill.objects.get(k_idorderbill = order_id)
      token = str(order.n_tokenorderbill)
      print(token)
      requestAPI = ApiTPaga()
      responseRevert = None
      responseRevert = requestAPI.revertir_pago(token)
      if "error_code" in responseRevert:
        print(responseRevert)
        
      statusResponse = responseRevert["status"]
      orderU = Orderbill.objects.filter(k_idorderbill = order_id).update(n_status= statusResponse[:3].upper())
      
      if statusResponse == 'reverted' :
        return render(request, 'petit/revertirTransaccion.html', {'message': 'La transacción fue revertida'})
      else :
        return render(request, 'petit/revertirTransaccion.html', {'message': 'La transacción no fue revertida . Intente de nuevo'})
    except Orderbill.DoesNotExist:
      raise Http404
      return redirect('petit/consultarTransacciones')

# Views relacionadas con los usuarios


def logout_view(request):
    logout(request)
    return redirect('login')
