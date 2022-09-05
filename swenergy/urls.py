from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView
from . import views

app_name = 'swenergy'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('detalhes/<int:pk>/', views.detalhes.as_view(), name='detalhes'),
]