from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.core.mail import send_mail

class GeraPDFMixin:
    def render_to_pdf(self, template_end, context_dict={}):
        template = get_template(template_end)
        html = template.render(context_dict)
        result = BytesIO()
        try:
            pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
            
            return HttpResponse(result.getvalue(), 
                                content_type='application/pdf')
        except Exception as e:
            print(e)
            return None

class Email:
    def send(self, assunto, mensagem, destino):
        send_mail(assunto, mensagem, 'equipe.swenergy@outlook.com', destino, fail_silently=False)



