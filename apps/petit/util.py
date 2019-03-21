from django.utils.timezone import now
from datetime import timedelta

def obtenerIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def obtenerFechaExpiracion():
    exp_date = now() + timedelta(days=1)
    return exp_date
