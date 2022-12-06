from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Sensor, Fase, Consumo, Predio
from .utils import GeraPDFMixin, Email
from django.db import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas

from django.http import HttpResponse, HttpRequest, JsonResponse
import json
from django.template.loader import get_template
from io import BytesIO
#import wget

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class index(View):
    #@csrf_exempt
    def get(self,request,*args,**kwargs):
        predios = Predio.objects.all()
        sensores = Sensor.objects.all()
        consumos = Consumo.objects.all()
        data = request.GET
        sec =  self.request.session
        json = models.JSONField(str(HttpRequest.body))

        url = '/'
        headers={'Content-Type': 'application/json'}
        #response = requests.get(url, headers=headers)
        #response = json.loads(response.content)

        #resultado = response
        
        #data = json.loads(request.body)

        #try:
            #data = json.loads(request.body)
            #label = data['label']
            #url = data ['url']
            #print label, url
        #except:
            #return HttpResponse("Malformed data!")
        #return HttpResponse("Got json data")
        contexto = {'predios':predios,'sensores':sensores, 'data':data, 'session':sec, 'args':args, 'kwargs':kwargs,'json':json, 'consumos':consumos}
        #contexto['resultado'] = resultado
        return render(request,'swenergy/index.html', contexto)
    @csrf_exempt
    def post(self,request,*args,**kwargs):
        contexto = {'data':request.POST, 'msg':'Metodo POST'}
        sensor = Sensor()
        pt      = request.POST['pt']
        qt      = request.POST['qt']
        st      = request.POST['st']
        itrms   = request.POST['itrms']
        pft     = request.POST['pft']
        freq    = request.POST['freq']
        ept     = request.POST['ept']
        eqt     = request.POST['eqt']
        yuaub   = request.POST['yuaub']
        yuauc   = request.POST['yuauc']
        yubuc   = request.POST['yubuc']
        tpsd    = request.POST['tpsd']
        return render(request,'swenergy/index.html',contexto)
@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class indexPredio(View):
    #@csrf_exempt
    def get(self,request,*args,**kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        contexto = {'predio':predio}
        return render(request,'swenergy/indexPredio.html', contexto)

    def post(self,request,*args,**kwargs):
        pass

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class detalhes(View):
    def get(self, request, *args, **kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        predio = sensor.predio
        return render(request, 'swenergy/detalhes.html', {'sensor':sensor, 'predio':predio})

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class detalhesPredio(View):
    def get(self, request, *args, **kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        return render(request, 'swenergy/detalhesPredio.html', {'predio':predio})

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class addSensor(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'swenergy/formSensor.html')
    
    def post(self, request, *args, **kwargs):
        sensor  = Sensor(titulo=request.POST['titulo'])
        sensor.save()
        fa      = Fase(tipo='A', sensor = sensor)
        fb      = Fase(tipo='B', sensor = sensor)
        fc      = Fase(tipo='C', sensor = sensor)
        fa.save()
        fb.save()
        fc.save()
        contexto = {'sensor':sensor, 'msg':'Sensor cadastrado!'}
        return render(request, 'swenergy/detalhes.html',contexto)
@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class addPredio(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'swenergy/formPredio.html')
    
    def post(self, request, *args, **kwargs):
        predio  = Predio(nome=request.POST['titulo'], Co2=request.POST['co2'], KWh=request.POST['kwh'],economico=request.POST['economico'],meta=request.POST['meta'], area=request.POST['area'], populacao=request.POST['pop'], pavimentos=request.POST['pav'], PotInst=request.POST['pi'], idade=request.POST['idade'] )
        geracaofv = request.POST.getlist('GFV')
        for gfv in geracaofv:
            if gfv=='1':
                predio.geracaoFV=True

            elif gfv=='2':

                predio.geracaoFV=False
            else:
                msg_erro = 'Dados inválidos!'
        predio.save()
        contexto = {'predio':predio, 'msg':'Edifício cadastrado!'}
        return render(request, 'swenergy/detalhesPredio.html',contexto)

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class editar(View):
    def get(self,request,*args,**kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        return render(request, 'swenergy/editar.html', {'sensor':sensor})
    def post(self,request,*args,**kwargs):
        sensor = get_object_or_404(Sensor, pk=request.POST['id'])
        sensor.titulo = request.POST['titulo']
        sensor.save()
        return render(request, 'swenergy/detalhes.html', {'sensor':sensor, 'msg_sucess':'Edições salvas!'})

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class editarPredio(View):
    def get(self,request,*args,**kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        return render(request, 'swenergy/editarPredio.html', {'predio':predio})
    def post(self,request,*args,**kwargs):
        predio = get_object_or_404(Predio, pk=request.POST['id'])
        predio.nome = request.POST['nome']
        predio.save()
        return render(request, 'swenergy/indexPredio.html', {'predio':predio, 'msg_sucess':'Edições salvas!'})

class cadastro(View):
    def get(self,request,*args,**kwargs):
        return render(request,'swenergy/cadastro.html')

    def post(self,request,*args,**kwargs):
        username = request.POST['username']
        nome = request.POST['nome']
        senha = request.POST['senha']

        user = User.objects.create_user(username, 'email', senha)
        user.first_name = nome
        user.save()
        sensores = Sensor.objects.all()
        return render(request, 'swenergy/index.html', {'sensores':sensores, 'msg_sucess':'sucesso'})

class IndexViewJSON(View):
    def get(self, request, *args, **kwargs):
        sensores = Sensor.objects.all()
        contexto = {'sensor_list': sensores}
        return render(
                    request, 'swenergy/data.json',contexto,
                    content_type='application/json'
                    )
                
class GetDataAPI(View):
    def get(self, request, *args, **kwargs):
        sensores = Sensor.objects.all()
        contexto = {'sensor_list': sensores}
        return JsonResponse(list(sensores.values()), safe = False)

class NiveisEnergia(View):
    def get(self, request, *args, **kwargs):        
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        predio = sensor.predio
        faseA = Fase.objects.get(tipo='A')
        faseB = Fase.objects.get(tipo='C')
        faseC = Fase.objects.get(tipo='B')
        return render(request, 'swenergy/niveis.html', {'predio':predio,'sensor':sensor, 'faseA':faseA, 'faseB':faseB, 'faseC':faseC})

class EnviarAlerta(View):
    def get(self, request, *args, **kwargs):
        msgRetorno = 'Email enviado com sucesso'
        email = Email()
        email.send('Teste de envio', 'Testando envio de email', ['deividson.silva@escolar.ifrn.edu.br'])
        try:
            email.send('Teste de envio', 'Testando envio de email', ['deividson.silva@escolar.ifrn.edu.br'])
        except:
            msgRetorno = 'Falha no envio'
        return render(request,'swenergy/index.html', {'msg':msgRetorno})


class RelatorioPDF(View, GeraPDFMixin):
    def get(self, request, *args, **kwargs):
        sensores = Sensor.objects.all()
        dados = {
            'sensores': sensores,
        }
        pdf = GeraPDFMixin()
        return pdf.render_to_pdf('swenergy/relatoriopdf.html', dados)

def GeraPDF(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    sensores = Sensor.objects.all()
    consumos = Consumo.objects.all()
    texto = list(sensores.values())
    template = get_template('swenergy/relatoriopdf.html')
    html = template.render({'sensores':sensores})
    p.drawString(10, 10, 
    "Lista de sensores: "
    )

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def get_relatorio(request):
    #wget.download("127.0.0.1:8000/relatoriopdf")
    return HttpResponse



