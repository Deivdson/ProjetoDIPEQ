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
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name_plural = 'Sensores'

class Fase(models.Model):
    #tipo    = ('A'),('B'),('C')
    tipo    = models.CharField(max_length=2, null=True)
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
    def __str__(self):
        return self.tipo

class Consumo(models.Model):
    data = models.DateTimeField()
    inicio = models.FloatField()
    fim = models.FloatField()
    total = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(('Sensor: {0} - Consumo: {1}').format(self.sensor, self.total))
