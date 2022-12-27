from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Sensor, Fase, Consumo, Predio, Custo
from .utils import GeraPDFMixin, Email
from django.db import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.http.request import QueryDict
import json, datetime
from calendar import monthrange
from django.template.loader import get_template
from io import BytesIO
#import wget

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

#Create your views here.
@method_decorator(
   login_required(login_url='/login'), name='dispatch'
)
class index(View):
    def get(self,request,*args,**kwargs):
        predios = Predio.objects.all()       
        contexto = {'predios':predios}

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
        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area

        mes = datetime.date.today().month
        consumos_diarios = Consumo.objects.filter(tipo='diario').filter(sensor=sensor)
        consumos_mensais = Consumo.objects.filter(tipo='mensal').filter(sensor=sensor).filter(data__icontains=mes)

        contexto = {
            'predio':predio,
            'consumos_diarios':consumos_diarios,
            'consumos_mensais':consumos_mensais, 
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area
            }
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

        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area

        consumos_diarios = Consumo.objects.filter(tipo='diario').filter(sensor=sensor)
        consumos_mensais = Consumo.objects.filter(tipo='mensal').filter(sensor=sensor)
        contexto = {
            'sensor':sensor,
            'predio':predio,
            'consumos_diarios':consumos_diarios,
            'consumos_mensais':consumos_mensais,
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area
        }
        return render(request, 'swenergy/detalhes.html', contexto)

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class detalhesPredio(View):
    def get(self, request, *args, **kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])

        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area

        contexto = {
            'predio':predio, 
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area
            }

        return render(request, 'swenergy/detalhesPredio.html', contexto)

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class addSensor(View):
    def get(self, request, *args, **kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area

        contexto = {
            'predio':predio, 
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area
            }
        return render(request, 'swenergy/formSensor.html', contexto)
    
    def post(self, request, *args, **kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        sensor  = Sensor(titulo=request.POST['titulo'], predio=predio)
        sensor.save()
        fa      = Fase(tipo='A', sensor = sensor)
        fb      = Fase(tipo='B', sensor = sensor)
        fc      = Fase(tipo='C', sensor = sensor)
        fa.save()
        fb.save()
        fc.save()

        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area
        contexto = {
            'sensor':sensor,
            'predio':predio, 
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area,
            'msg':'Sensor cadastrado!'
            }
        return render(request, 'swenergy/detalhes.html',contexto)
@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class addPredio(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'swenergy/formPredio.html')
    
    def post(self, request, *args, **kwargs):
        predio  = Predio(
            nome        = request.POST['titulo'],
            KWh         = request.POST['kwh'],
            economico   = request.POST['economico'],
            meta        = request.POST['meta'],
            area        = request.POST['area'], 
            populacao   = request.POST['pop'], 
            pavimentos  = request.POST['pav'], 
            PotInst     = request.POST['pi'], 
            tarifaFP    = request.POST['tarifaFP'],
            idade       = request.POST['idade'] 
            )
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
        predio = sensor.predio

        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area
        
        contexto = {
            'sensor':sensor,
            'predio':predio, 
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area,            
            }
        return render(request, 'swenergy/editar.html', contexto)
    def post(self,request,*args,**kwargs):
        sensor = get_object_or_404(Sensor, pk=request.POST['id'])
        sensor.titulo = request.POST['titulo']
        sensor.save()

        predio = sensor.predio

        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area

        consumos_diarios = Consumo.objects.filter(tipo='diario').filter(sensor=sensor)
        consumos_mensais = Consumo.objects.filter(tipo='mensal').filter(sensor=sensor)
        
        contexto = {
            'sensor':sensor,            
            'predio':predio,
            'consumos_diarios':consumos_diarios,
            'consumos_mensais':consumos_mensais, 
            'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area,
            'msg_sucess':'Edições salvas!',            
            }
        return render(request, 'swenergy/detalhes.html', contexto)

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
        
        predio.KWh = request.POST['kwh']
        predio.economico = request.POST['economico']
        predio.meta = request.POST['meta']
        predio.area = request.POST['area']
        predio.populacao = request.POST['pop']
        predio.pavimentos = request.POST['pop']
        predio.PotInst = request.POST['pav']
        predio.geracaoFV = request.POST['pi']
        predio.idade = request.POST['idade']
        predio.save()                                
        return render(request, 'swenergy/indexPredio.html', {'predio':predio, 'msg_sucess':'Edições salvas!'})

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class ExcluirPredio(View):
    def get(self,request, **kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        predio.delete()

@method_decorator(
    login_required(login_url='/login'), name='dispatch'
)
class ExcluirSensor(View):
    def get(self,request, **kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        sensor.delete()

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
        consumo = Consumo.objects.all()
        contexto = {'sensor_list': sensores}
        lista = list(sensores.values())
        #lista.append(list(consumo.values()))
        return JsonResponse(lista, safe = False)

class GetSensorDataAPI(View):
    def get(self, request, *args, **kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        sensores = Sensor.objects.filter(pk=kwargs['pk'])

        fases = Fase.objects.filter(sensor=sensor).order_by('tipo')
        lista = list(sensores.values())
        #lista.append(list(fases.values()))
        contexto = {'sensor': sensor, 'fases':fases}
        return JsonResponse(lista, safe = False)

class GetFaseDataAPI(View):
    def get(self, request, *args, **kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        fases = Fase.objects.filter(sensor=sensor).order_by('tipo')
        lista = list(fases.values())
        contexto = {'sensor': sensor, 'fases':fases}
        return JsonResponse(lista, safe = False)

class NiveisEnergia(View):
    def get(self, request, *args, **kwargs):        
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        predio = sensor.predio
        faseA = Fase.objects.filter(tipo='A').filter(sensor=sensor)
        faseB = Fase.objects.filter(tipo='B').filter(sensor=sensor)
        faseC = Fase.objects.filter(tipo='C').filter(sensor=sensor)

        consumo_mes = 0
        for sensor in predio.sensor_set.all():
            for consumo in sensor.consumo_set.all():
                if consumo.total:
                    consumo_mes =consumo_mes + float(consumo.total)
        
        consumo_pessoa = consumo_mes/predio.populacao
        consumo_area = consumo_mes/predio.area
        contexto = {
            'predio':predio,'sensor':sensor, 
            'faseA':faseA,'faseB':faseB, 
            'faseC':faseC,'consumo_mes':consumo_mes, 
            'consumo_pessoa':consumo_pessoa, 
            'consumo_area':consumo_area
            }
        return render(request, 'swenergy/niveis.html', contexto)

class Eficiencia(View):
    def get(self,request,*args,**kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])
        return render(request, 'swenergy/eficiencia.html', {'predio':predio})
    def post(self,request,*args,**kwargs):
        predio = get_object_or_404(Predio, pk=request.POST['id'])
    
        predio.Iluminacao   = request.POST['Iluminacao']
        predio.CondAr       = request.POST['CondAr']
        predio.envoltoria   = request.POST['envoltoria']
        predio.save()
        return render(request, 'swenergy/indexPredio.html', {'predio':predio, 'msg_sucess':'Edições salvas!'})

class Contas(View):
    def get(self, request, *args, **kwargs):
        predio = get_object_or_404(Predio, pk=kwargs['pk'])        
        return render(request, 'swenergy/contas.html', {'predio':predio})

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
        data = datetime.datetime.now()
        predio = get_object_or_404(Predio, pk=kwargs['pk'])        
        dados = {
            'predio':predio,
            'data': data,
        }
        pdf = GeraPDFMixin()
        return pdf.render_to_pdf('swenergy/relatoriopdf.html', dados)

class Controller(View):
    def get(self,request, *args,**kwargs):
        now = datetime.datetime.now()
        date = datetime.date.today()
        last_day = date.replace(day=monthrange(date.year, date.month)[1])

        data = request.GET
        dict = QueryDict('', mutable=True)
        dict.update(data)
        print(dict)
        
        sensor = get_object_or_404(Sensor, pk=1)
        predio = sensor.predio

        if data:
            sensor.pt       = data.getlist('pt')[0]
            sensor.qt       = data.getlist('qt')[0]
            sensor.st       = data.getlist('st')[0]
            sensor.itrms    = data.getlist('itrms')[0]
            sensor.pft      = data.getlist('pft')[0]
            sensor.freq     = data.getlist('freq')[0]
            sensor.ept      = data.getlist('ept')[0]
            sensor.eqt      = data.getlist('eqt')[0]
            sensor.yuaub    = data.getlist('yuaub')[0]
            sensor.yuauc    = data.getlist('yuauc')[0]
            sensor.yubuc    = data.getlist('yubuc')[0]
            sensor.tpsd     = data.getlist('tpsd')[0]

            hora = now.strftime('%H:%M')
            alerta_mensal  = 0
            consumo_do_dia = Consumo.objects.filter(data=date).filter(tipo='diario').filter(sensor=sensor).first()
            consumo_mes = Consumo.objects.filter(data=date).filter(tipo='mensal').filter(sensor=sensor).first()
            if hora == "00:00" and not(consumo_do_dia):
                consumo = Consumo(data=date, inicio=data.getlist('ept')[0], sensor=sensor)
                consumo.save()      
                consumo_mes = Consumo(data=date, total=0, tipo='mensal', sensor=sensor)
                consumo_mes.save()          

            if hora == "23:59" and consumo_do_dia:            
                consumo_do_dia.fim = data.getlist('ept')[0]
                consumo_do_dia.total = (consumo.fim - consumo.inicio)/100
                consumo_do_dia.save()
                                              
                consumo_mes.total += consumo.total
                alerta_mensal = consumo_mes.total
                consumo_mes.save()
                if date == last_day:
                    custo = Custo(consumo=consumo_mes, FP=(predio.tarifaFP*consumo_mes.total))
                    custo.save()
        sensor.save()

        if date.weekday()<5 and (float(sensor.ept) >= 600 or alerta_mensal>10000):
            msgRetorno = 'Um alerta foi emitido.'
            email = Email()
            try:
                email.send('Alerta de Consumo!', '{0}\nO consumo está acima dos níveis normais. Consumo total do dia: {1}/600 Consumo do mês: {2}/10000'.format((date.strftime('%d/%m/%y')), sensor.ept, alerta_mensal), ['deividson.silva@escolar.ifrn.edu.br'])
            except:
                msgRetorno = 'Falha no envio de alerta'
                print(msgRetorno)

        elif date.weekday()>4 and (float(sensor.ept) >= 150 or alerta_mensal>10000):
            msgRetorno = 'Um alerta foi emitido.'
            email = Email()
            try:
                email.send('Alerta de Consumo!', '{0}\nO consumo está acima dos níveis normais. Consumo total do dia: {1}/150 Consumo do mês: {2}/10000'.format((date.strftime('%d/%m/%y')), sensor.ept, alerta_mensal), ['deividson.silva@escolar.ifrn.edu.br'])
            except:
                msgRetorno = 'Falha no envio de alerta'
                print(msgRetorno)

        return HttpResponse

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

def ConsumoMensal(self, predio):
    consumo_mes = 0
    for sensor in predio.sensor_set.all():
        for consumo in sensor.consumo_set.all():
            if consumo.total:
                consumo_mes =consumo_mes + float(consumo.total)
    return consumo_mes
        
        


