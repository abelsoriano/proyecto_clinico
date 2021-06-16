# Django
from django.utils.timezone import localtime, now


def contexto_general(request):
    """ Extiende el contexto de todas las plantillas """
    ctx = {
        'date': localtime(now()).date()
    }
    return ctx
