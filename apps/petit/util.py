from django.utils.timezone import now
from datetime import timedelta
import datetime


def obtenerIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def obtenerFechaExpiracion():
    exp_date = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc) + timedelta(days=1)
    exp_date = exp_date.isoformat()
    return exp_date
