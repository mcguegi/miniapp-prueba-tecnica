import requests
import base64
import secrets
import json
from django.conf import settings


class ApiTPaga:

    # Cabeceras
    def __init__(self):

        #Se codifica el usuario y la contraseña del API en base64 y posteriormente se convierte a string para poder ponerlo en la cabecera de autorizacion
        auth_encode = base64.b64encode(
            bytes(str(settings.TPAGA_API_USER+':'+settings.TPAGA_API_PASSWORD), 'utf-8'))
        auth_var = auth_encode.decode('ascii')


        self.headers = {
            'Authorization': 'Basic ' + str(auth_var),
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json'
        }

    # Metodo que solicitara a la API el pago de una orden

    def solicitar_hacer_pago(self, order_id, user_ip_address, terminal_id, arr_items, total_amount, expiration_date):
        # Se organizan en un diccionario la información de la orden para solicitar el pago
        datos_solicitud_pago = {
            'cost': int(total_amount),
            'purchase_details_url': '',
            'voucher_url': '',
            'idempotency_token': secrets.token_hex(16),
            'order_id': order_id,
            'terminal_id': terminal_id,
            'purchase_description': 'Compra en comercio de mascotas PetIT',
            'purchase_items': arr_items,
            'user_ip_address': user_ip_address,
            'expires_at': expiration_date
        }

        # Formatea el objeto datos_solicitud_pago para que sea un JSON
        datos_solicitud_pago = json.dumps(datos_solicitud_pago, ensure_ascii=False)

        # Se accede al endpoint para crear una solicitud de pago
        url_sol_pago = settings.TPAGA_URL_API+'/create'

        # Se intenta hacer la petición POST al API con los el JSON a la url_sol_pago , si esto no funciona entra al catch y reporta el error
        try:
            res = requests.post(url_sol_pago, data=datos_solicitud_pago, headers=self.headers)
        except requests.exceptions.RequestException as error:
            raise error

        # La TPaga API devuelve un JSON con la información de la solicitud y la tpaga_payment_url
        respuesta = res.json()

        return respuesta


    def confirmar_estado_sol_pago (self, token) :

        # Se intenta acceder al API con el token de una solicitud de pago
        URL_confirmacion_estado = settings.TPAGA_URL_API + '/' + token + '/info'
        try:
            res = requests.get(URL_confirmacion_estado , headers=self.headers)
        except requests.exceptions.RequestException as error:
            raise error

        # La respuesta es un JSON y dentro tiene una clave 'status' que tiene el estado de la solicitud de pago
        respuesta = res.json()

        return respuesta


    def confirmar_entrega (self, token):
        # Endpoint para notificar explicitamente a TPaga de la entrega del producto/servicio
        URL_confirmacion_estado = settings.TPAGA_URL_API + '/confirm_delivery'

        # se envia el token del payment_request y se formatea como JSON
        datos_solicitud = {'payment_request': token}
        datos_solicitud = json.dumps(datos_solicitud, ensure_ascii=False)

        # Realizo la peticion POST a la API para que la entrega sea confirmada
        try:
            res = requests.post(URL_confirmacion_estado , data=datos_solicitud, headers = self.headers)
        except requests.exceptions.RequestException as error:
            raise error 

        # TPaga API devuelve un json con la informacion y el status actualizado
        respuesta = res.json()

        return respuesta

    def revertir_pago(self, token):
        # Endpoint para notificar explicitamente a TPaga de la entrega del producto/servicio
        URL_confirmacion_estado = settings.TPAGA_URL_API + '/confirm_delivery'

        # se envia el token del payment_request y se formatea como JSON
        datos_solicitud = {'payment_request': token}
        datos_solicitud = json.dumps(datos_solicitud, ensure_ascii=False)

        # Realizo la peticion POST a la API para que la entrega sea confirmada
        try:
            res = requests.post(URL_confirmacion_estado , data=datos_solicitud, headers = self.headers)
        except requests.exceptions.RequestException as error:
            raise error 

        # TPaga API devuelve un json con la informacion y el status actualizado
        respuesta = res.json()
        
        return respuesta