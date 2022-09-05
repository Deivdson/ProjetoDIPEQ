from django.db import models

from django.utils import timezone
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Sensor(models.Model):
    titulo  = models.CharField(max_length=50)
    time    = models.TimeField()        # h m s
    pt      = models.FloatField()       # Potência ativa total
    qt      = models.FloatField()       # Potência reativa total
    st      = models.FloatField()       # Potência aparente total 
    itrms   = models.FloatField()       # Corrente total
    pft     = models.FloatField()       # Fator de potência total
    freq    = models.FloatField()       # Frequência
    ept     = models.FloatField()       # Consumo de energia ativa total
    eqt     = models.FloatField()       # Consumo de energia reativa total      
    yuaub   = models.FloatField()       # Ângulo entre Tensão Fase A e Fase B
    yuauc   = models.FloatField()       # Ângulo entre Tensão Fase B e Fase C
    yubuc   = models.FloatField()       # Ângulo entre Tensão Fase B e Fase C
    tpsd    = models.FloatField()       # Temperatura

class Fase(models.Model):
    tipo    = ('A'),('B'),('C')
    p       = models.FloatField()       # Potência ativa
    q       = models.FloatField()       # Potência reativa
    s       = models.FloatField()       # Potência aparente
    urms    = models.FloatField()       # Tensão
    itrms   = models.FloatField()       # Corrente
    pf      = models.FloatField()       # Fator de potência 
    pg      = models.FloatField()       # Ângulo entre a tensão e corrente
    ep      = models.FloatField()       # Consumo de energia ativa
    eq      = models.FloatField()       # Consumo de eneergia reativa
    sensor  = models.ForeignKey(Sensor, on_delete = models.CASCADE, null=True) 
