from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Sensor, Fase

# Create your views here.
class index(View):
    def get(self,request,*args,**kwargs):
        sensores = Sensor.objects.all()
        return render(request,'swenergy/index.html', {'sensores':sensores})
    
    def post(self,request,*args,**kwargs):
        contexto = {'msg':'POST'}
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
        yubuc   = reques.POST['yubuc']
        tpsd    = request.POST['tpsd']
        return render(request,'swenergy/index.html',contexto)

class detalhes(View):
    def get(self, request, *args, **kwargs):
        sensor = get_object_or_404(Sensor, pk=kwargs['pk'])
        return render(request, 'swenergy/detalhes.html', {'sensor':sensor})

