from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView
from . import views

app_name = 'swenergy'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('data/', views.IndexViewJSON.as_view(), name='index_json'),
    path('api/data/', views.GetDataAPI.as_view(), name='get_data'),
    path('detalhes/<int:pk>/', views.detalhes.as_view(), name='detalhes'),
    path('addSensor/', views.addSensor.as_view(), name='addSensor'),
    path('editar/<int:pk>/', views.editar.as_view(), name='editar'),
    path('cadastro/', views.cadastro.as_view(), name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='swenergy/login.html'), name = 'login')
]