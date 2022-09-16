from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Sensor, Fase, Consumo
from django.db import models

# Create your views here.
class index(View):
    def get(self,request,*args,**kwargs):
        sensores = Sensor.objects.all()
        consumos = Consumo.objects.all()
        data = request.GET
        sec =  self.request.session
        json = models.JSONField(request.GET)
        contexto = {'sensores':sensores, 'data':data, 'session':sec, 'args':args, 'kwargs':kwargs,'json':json, 'consumos':consumos}

        return render(request,'swenergy/index.html', contexto)
    
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


class detalhes(View):
    def get(self, request, *args, **kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        return render(request, 'swenergy/detalhes.html', {'sensor':sensor})

class addSensor(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'swenergy/formSensor.html')
    
    def post(self, request, *args, **kwargs):
        sensor  = Sensor(titulo=request.POST['titulo'])
        fa      = Fase(tipo='A', sensor = sensor)
        fb      = Fase(tipo='B', sensor = sensor)
        fc      = Fase(tipo='C', sensor = sensor)
        contexto = {'sensor':sensor, 'msg':'Sensor cadastrado!'}
        return render(request, 'swenergy/detalhes.html',contexto)

class editar(View):
    def get(self,request,*args,**kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        return render(request, 'swenergy/editar.html', {'sensor':sensor})
    def post(self,request,*args,**kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs[request.POST['id']])
        sensor.titulo = request.POST['titulo']
        sensor.save()
        return render(request, 'swenergy/detalhes.html', {'sensor':sensor, 'msg_sucess':'Edições salvas!'})
