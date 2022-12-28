from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView

from swenergy.utils import GeraPDFMixin
from . import views

app_name = 'swenergy'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('data/', views.IndexViewJSON.as_view(), name='index_json'),
    path('api/data/sensor/<int:pk>/', views.GetSensorDataAPI.as_view(), name='get_sensor_data'),
    path('api/data/fase/<int:pk>/', views.GetFaseDataAPI.as_view(), name='get_sensor_data'),
    path('api/data/', views.GetDataAPI.as_view(), name='get_data'),

    path('detalhes/<int:pk>/', views.detalhes.as_view(), name='detalhes'),
    path('addSensor/<int:pk>/', views.addSensor.as_view(), name='addSensor'),
    path('editar/<int:pk>/', views.editar.as_view(), name='editar'),
    path('cadastro/', views.cadastro.as_view(), name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='swenergy/login.html'), name = 'login'),

    path('indexPredio/<int:pk>/', views.indexPredio.as_view(), name='indexPredio'),
    path('addPredio/', views.addPredio.as_view(), name='addPredio'),
    path('editarPredio/<int:pk>/', views.editarPredio.as_view(), name='editarPredio'),
    path('detalhesPredio/<int:pk>/', views.detalhesPredio.as_view(), name='detalhesPredio'),

    path('niveis/<int:pk>/', views.NiveisEnergia.as_view(), name='niveis'),
    path('eficiencia/<int:pk>/', views.Eficiencia.as_view(), name='eficiencia'),
    path('contas/<int:pk>/', views.Contas.as_view(), name='contas'),
    #testePDF
    path('relatorio/', views.GeraPDF, name='relatorio'),
    #SerializadorPDF
    path('relatoriopdf/<int:pk>/', views.RelatorioPDF.as_view(), name='relatoriopdf'),
    #Baixar relatorio
    path('getRelatorio/', views.get_relatorio, name='getRelatorio'),

    #alertas
    path('enviarAlerta/', views.EnviarAlerta.as_view(), name='alerta'),
    path('api/sensor/', views.Controller.as_view(), name='controller')
]