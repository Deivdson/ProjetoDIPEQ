from django.db import models

from django.utils import timezone
import datetime
from django.contrib.auth.models import User
# Create your models here.
class Predio(models.Model):
    nome = models.CharField(max_length=50)
    Co2 = models.FloatField(null=True) # ambienteal
    KWh = models.FloatField(null=True) #KWh por mes
    economico = models.FloatField(null=True)
    meta = models.FloatField(null=True)

    area = models.FloatField(null=True)
    pupulacao = models.FloatField(null=True)
    pavimentos = models.FloatField(null=True)
    PotInst = models.FloatField(null=True)
    geracaoFV = models.BooleanField(default=False)
    idade = models.IntegerField(null=True)


class Sensor(models.Model):
    titulo  = models.CharField(max_length=50)
    time    = models.TimeField(null=True)        # h m s
    pt      = models.FloatField(null=True)       # Potência ativa total
    qt      = models.FloatField(null=True)       # Potência reativa total
    st      = models.FloatField(null=True)       # Potência aparente total 
    itrms   = models.FloatField(null=True)       # Corrente total
    pft     = models.FloatField(null=True)       # Fator de potência total
    freq    = models.FloatField(null=True)       # Frequência
    ept     = models.FloatField(null=True)       # Consumo de energia ativa total
    eqt     = models.FloatField(null=True)       # Consumo de energia reativa total      
    yuaub   = models.FloatField(null=True)       # Ângulo entre Tensão Fase A e Fase B
    yuauc   = models.FloatField(null=True)       # Ângulo entre Tensão Fase B e Fase C
    yubuc   = models.FloatField(null=True)       # Ângulo entre Tensão Fase B e Fase C
    tpsd    = models.FloatField(null=True)       # Temperatura
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name_plural = 'Sensores'

class Fase(models.Model):
    #tipo    = ('A'),('B'),('C')
    tipo    = models.CharField(max_length=2, null=True)
    p       = models.FloatField(null=True)       # Potência ativa
    q       = models.FloatField(null=True)       # Potência reativa
    s       = models.FloatField(null=True)       # Potência aparente
    urms    = models.FloatField(null=True)       # Tensão
    itrms   = models.FloatField(null=True)       # Corrente
    pf      = models.FloatField(null=True)       # Fator de potência 
    pg      = models.FloatField(null=True)       # Ângulo entre a tensão e corrente
    ep      = models.FloatField(null=True)       # Consumo de energia ativa
    eq      = models.FloatField(null=True)       # Consumo de energia reativa
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
        return ('Sensor: {0} - Consumo: {1}').format(self.sensor, self.total)


