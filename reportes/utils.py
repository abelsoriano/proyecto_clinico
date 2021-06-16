# Python
from io import BytesIO

# Django
from django.template.loader import get_template
from django.http import HttpResponse

# xhtml2pdf
from xhtml2pdf import pisa

def generar_reporte_pdf(plantilla_fuente, contexto={}):
    plantilla = get_template(plantilla_fuente)
    html = plantilla.render(contexto)
    result = BytesIO()
    reporte_pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)
    if not reporte_pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None